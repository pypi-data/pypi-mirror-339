from .filetypes import DataType
import geopandas as gpd
import logging
import duckdb
from ..utils import authenticate_duckdb_connection
import uuid
import copy
import s3fs
from tqdm import tqdm
import pyarrow.parquet as pq
from ..geoduck import GeoDuck2


def dummy_tqdm(x, *args, **kwargs):
    return x


class IntakeQueryBuilder:
    """
    Builds a query to read a spatial dataset from a file or GeoDataFrame.
    """
    default_copy_options = {"FORMAT": "'PARQUET'", "COMPRESSION": "'ZSTD'"}
    
    def __init__(
        self, 
        parquet_path: str,
        data: str | gpd.GeoDataFrame | None = None, 
        partition_by: list[str] = [],
        append_partition_column: str | None = None,
        layer: str | None = None,
    ):
        self.data = data
        self.parquet_path = parquet_path
        self.partition_by = partition_by
        self.append_partition_column = append_partition_column
        self.data_type = DataType.from_extension(data)
        self.layer = layer
        
    def get_from_target(self):
        return f"st_read('{self.data}'{f", layer='{self.layer}'" if self.layer else ""})"
    
    def get_partition_clause(self):
        partition_by = copy.deepcopy(self.partition_by)
        if self.append_partition_column:
            partition_by.append(self.append_partition_column)
            
        if len(partition_by) > 0:
            return ", ".join(partition_by)
        else:
            return None
        
    def get_copy_options(self):
        copy_options = copy.deepcopy(self.default_copy_options)
        pc = self.get_partition_clause()
        if pc:
            copy_options.update(
                {"PARTITION_BY": f"({pc})", "FILENAME_PATTERN": "'data_{uuid}'"}
            )
        return copy_options
    
    
class Intake:
    def __init__(self, geoduck: GeoDuck2):
        self.geoduck = geoduck
        
    def gdf_to_parquet(
        self,
        gdf: gpd.GeoDataFrame,
        parquet_path: str,
        partition_by: list[str] = [],
        overwrite: bool = False,
        append_partition_id: str | None = None,
        append_partition_column: str | None = None,
    ):
        
        if overwrite:
            logging.warning("overwriting the existing parquet file")
            fs = s3fs.S3FileSystem()
            if fs.exists(parquet_path):
                fs.rm(parquet_path, recursive=True)
        
        df_copy = gdf.copy()
        df_copy["geometry_wkb"] = df_copy.geometry.apply(lambda geom: geom.wkb)
        df_copy = df_copy.drop(columns=["geometry"])
        tmp_table_name = f"tmp_table_{str(uuid.uuid4()).split('-')[0]}"
        self.geoduck.con.register(tmp_table_name, df_copy)
        
        additional_partition_clause = f"'{append_partition_id}' as {append_partition_column}" if append_partition_id else ""
        
        query_builder = IntakeQueryBuilder(
            parquet_path=parquet_path,
            data=df_copy,
            partition_by=partition_by,
            append_partition_column=append_partition_column,
        )
        
        copy_options = query_builder.get_copy_options()
        
        if not overwrite:
            copy_options["APPEND"] = "TRUE"
        
        options_str = ", ".join(f"{k} {v}" for k, v in copy_options.items())
        
        sql = f"""
            COPY (
                SELECT * EXCLUDE (geometry_wkb), ST_GeomFromWKB(geometry_wkb) as geometry, {additional_partition_clause}
                FROM (
                    SELECT *
                    FROM {tmp_table_name}
                )
            )
            TO '{parquet_path}'
            ({options_str})
        """
        logging.info(sql)
        self.geoduck.sql_with_retries(sql)
        crs = gdf.crs
        pi = self.geoduck.parquet_file_to_info(parquet_path)
        self.geoduck.create_view(pi.view_name, pi.parquet_file.path, is_partitioned=len(partition_by) > 0 or append_partition_id, exists_ok = True)
        self.geoduck.insert_metadata(pi.view_name, crs)
        
        
    def ogr_to_parquet(
        self,
        ogr_path: str,
        parquet_path: str,
        layer: str = None,
        partition_by: list[str] = [],
        limit: int = None,
        overwrite: bool = False,
        append_partition_id: str | None = None,
        append_partition_column: str | None = None,
        partition_batch_to_manage_memory: bool = False,
        show_progress: bool = False,
        batch_size: int | None = None,
        retries: int = 3,
    ):
        """
        Save a GeoPackage file to (partitioned) parquet using DuckDB with GeoParquet metadata.
        """
        assert DataType.is_supported(ogr_path), f"File type {DataType.from_extension(ogr_path)} is not supported"
        
        if overwrite and append_partition_id:
            logging.warning("append_partition_id is not supported with overwrite, ignoring append_partition_id")

        if append_partition_id and not append_partition_column:
            raise ValueError("append_partition_column is required when append_partition_id is provided")
        
        if overwrite:
            logging.warning("overwriting the existing parquet file")
            if self.geoduck.fs.exists(parquet_path):
                logging.info(f"removing {parquet_path}")
                self.geoduck.fs.rm(parquet_path, recursive=True)
                
        if show_progress:
            _tqdm = tqdm
            self.geoduck.con.execute('SET enable_progress_bar=false')
        else:
            _tqdm = dummy_tqdm
        
        query_builder = IntakeQueryBuilder(
            data=ogr_path,
            parquet_path=parquet_path,
            partition_by=partition_by,
            append_partition_column=append_partition_column,
            layer=layer,
        )
        
        from_target = query_builder.get_from_target()
        partition_cols = query_builder.get_partition_clause()
        copy_options = query_builder.get_copy_options()
        
        if partition_batch_to_manage_memory:
            if limit:
                logging.warning("partition_batch_to_manage_memory is not supported with limit.  Ignoring limit.")
            
            self.geoduck.con.sql(
                f"""
                    CREATE TABLE partitions AS
                    SELECT DISTINCT {partition_cols} FROM {from_target}
                """
            )
            
            n_partitions = self.geoduck.con.sql(
                f"""
                    SELECT COUNT(*) FROM partitions
                """
            ).fetchone()[0]
            logging.info(f"Number of partitions: {n_partitions}")
            
            # This is implemented as a for loop for memory management.  May be unnecessary in the future.
            for i in _tqdm(range(n_partitions), desc="Uploading partitions"):
                if i == 1 or not overwrite:
                    copy_options["APPEND"] = "TRUE"
                
                options_str = ", ".join(f"{k} {v}" for k, v in copy_options.items())
                
                inner_sql = f"""
                    SELECT * 
                    FROM {from_target}
                    JOIN (
                        SELECT * FROM partitions
                        LIMIT 1
                        OFFSET {i}
                    ) AS p
                    USING ({partition_cols})
                """
                
                sql = f"""
                    COPY (
                        SELECT * EXCLUDE (geom), geom as geometry, '{append_partition_id}' as {append_partition_column}
                        FROM (
                            SELECT *
                            FROM ({inner_sql})
                        )
                    )
                    TO '{parquet_path}'
                    ({options_str})
                """
                self.geoduck.sql_with_retries(sql, retries)
            
        else:
            append_partition_clause = ""
            if append_partition_id:
                copy_options["APPEND"] = "TRUE"
                append_partition_clause = f", '{append_partition_id}' as {append_partition_column}"
                
                
            options_str = ", ".join(f"{k} {v}" for k, v in copy_options.items())
            
            n = self.geoduck.con.sql(f"SELECT COUNT(*) FROM {from_target}").fetchone()[0]
            logging.info(f"Number of rows: {n}")
            if batch_size and batch_size < n:
                for i in range(0, n, batch_size):
                    sql = f"""
                    COPY (
                        SELECT * EXCLUDE (geom), geom as geometry {append_partition_clause}
                        FROM (
                            SELECT *
                            FROM {from_target}
                        )
                        LIMIT {batch_size}
                        OFFSET {i}
                    )
                    TO '{parquet_path}'
                    ({options_str})
                    """
                    self.geoduck.sql_with_retries(sql, retries)
            else:
                sql = f"""
                    COPY (
                        SELECT * EXCLUDE (geom), geom as geometry {append_partition_clause}
                        FROM {from_target}
                    )
                    TO '{parquet_path}'
                    ({options_str})
                """
                self.geoduck.sql_with_retries(sql, retries)
        
        