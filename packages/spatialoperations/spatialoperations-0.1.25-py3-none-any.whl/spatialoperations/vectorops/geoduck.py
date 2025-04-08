import duckdb
import logging
import geopandas as gpd
from typing import Union
import s3fs
import os
from dataclasses import dataclass
import uuid
from .storage import write_view_to_parquet
from .utils import register_gdf_to_duckdb, authenticate_duckdb_connection
import time
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DEFAULT_LAYER_CREATION_OPTIONS = {
    "MINZOOM": 10,
    "MAXZOOM": 15,
    "SRS": "EPSG:4326"
}

def create_connection(progress_bar: bool = False):
    con = duckdb.connect()
    con.install_extension("spatial")
    con.load_extension("spatial")
    if not progress_bar:
        con.execute('SET enable_progress_bar=false')
    authenticate_duckdb_connection(con)
    return con


def sql_with_retries(con, sql, retries=3, time_between_retries=4):
    for i in range(retries):
        try:
            res = con.sql(sql)
            if retries > 1:
                logging.info(f"Success after {i} retries")
            return res
        except Exception as e:
            logging.info(e)
            logging.info(f"Retrying {i + 1} of {retries}")
            if i == retries - 1:
                raise e
            time.sleep(time_between_retries)
            continue


@dataclass  
class ParquetFile:
    is_partitioned: bool
    path: str
    
@dataclass
class ParquetView:
    view_name: str
    parquet_file: ParquetFile

class GeoDuck2:
    """
    A class for working with geospatial data using DuckDB.
    """
    def __init__(self, directory: str):
        """
        Initialize a GeoDuck2 instance.
    """ 
        self.con = create_connection()
        if directory.endswith("/"):
            directory = directory[:-1]
        self.fs = s3fs.S3FileSystem()
        self.directory = directory
        self.metadata_path = f"{self.directory}/metadata.parquet"
        
        self.create_metadata_table_if_not_exists()
        self.populate_database()
        
    def create_metadata_table_if_not_exists(self):
        """
        Check if the metadata table exists.
        """
        """
        Check if the metadata table exists. If not, create it with 'view' and 'crs' columns.
        
        Args:
            path: Path to the metadata parquet file
            
        Returns:
            bool: True if the metadata table exists, False otherwise
        """
        
        if not self.fs.exists(self.metadata_path):
            # Create metadata table with view and crs columns
            self.con.sql("""
                CREATE TABLE metadata_table (
                    view VARCHAR,
                    crs VARCHAR
                )
            """)
            
            # Copy the table to parquet
            self.con.sql(f"""
                COPY metadata_table TO '{self.metadata_path}'
                (FORMAT 'PARQUET', COMPRESSION 'ZSTD')
            """)
            
            self.con.sql(f"""
                CREATE VIEW metadata AS
                SELECT * FROM read_parquet('{self.metadata_path}')
            """)
            
            
    def insert_metadata(self, view: str, crs: str):
        """
        Insert metadata into the metadata table.
        """
        self.con.sql(f"""
            INSERT INTO metadata_table (view, crs) VALUES ('{view}', '{crs}')
        """)
        self.con.sql(f"""
            COPY metadata_table TO '{self.metadata_path}'
            (FORMAT 'PARQUET', COMPRESSION 'ZSTD', OVERWRITE TRUE)
        """)
    
    def parquet_file_to_info(self, path: str):
        """
        Convert a parquet file to a ParquetView.
        """
        is_partitioned = path.count(".parquet") > 1
        partitioned_root = path.split(".parquet")[0] + ".parquet"
        view_name = path.split("/")[-1].split(".")[0]
        
        return ParquetView(
            parquet_file=ParquetFile(
                is_partitioned=is_partitioned, 
                path=f"s3://{partitioned_root}" if "s3://" not in partitioned_root else partitioned_root
            ),
            view_name=view_name
        )
    
    def get_parquet_info(self, path: str | None = None, traverse_subfolders: bool = True):
        """
        Get all parquet files in the given path.
        """
        is_partitioned = lambda file: file.count(".parquet") > 1
        partitioned_root = lambda file: file.split(".parquet")[0] + ".parquet"
        
        if traverse_subfolders:
            suffix = "/**/*.parquet"
        else:
            suffix = "/*.parquet"
        
        if path is None:
            parquet_files = self.fs.glob(f"{self.directory}{suffix}")
        else:
            parquet_files = self.fs.glob(f"{self.directory}/{path}{suffix}")
            
        return [
            ParquetView(
                parquet_file=ParquetFile(
                    is_partitioned=is_part,
                    path=f"s3://{root_path}",
                ),
                view_name=root_path.split("/")[-1].split(".")[0]
            )
            for is_part, root_path in list(set([(
                is_partitioned(file),
                partitioned_root(file)
            ) for file in parquet_files]))
        ]
        
    def create_view(self, view_name: str, path: str, is_partitioned: bool, exists_ok: bool = True):
        """
        Create a view from a parquet file.
        """
        if is_partitioned:
            suffix = "/**/*.parquet"
        else:
            suffix = ""
        
        if exists_ok:
            exists_clause = "IF NOT EXISTS"
        else: 
            exists_clause = ""
            
        sql = f"""
            CREATE VIEW {exists_clause} {view_name} AS 
            SELECT * FROM read_parquet('{path}{suffix}');
        """
        self.sql_with_retries(sql)
        
    def populate_database(self, path: str | None = None):
        """
        Populate the database with the parquet files.
        """
        for parquet in self.get_parquet_info():
            self.create_view(
                view_name=parquet.view_name,
                path=parquet.parquet_file.path,
                is_partitioned=parquet.parquet_file.is_partitioned
            )
    
    def get_views(self, as_list: bool = False):
        """
        Get all views in the database.
        """
        sql = """
            SELECT * EXCLUDE(sql)
            FROM duckdb_views()
            WHERE NOT internal;
        """
        results = self.con.sql(sql)
        if as_list:
            return [i[0] for i in list(results["view_name"].fetchall())]
        return results
    
    def get_crs(self, view: str):
        sql = f"SELECT crs FROM metadata WHERE view = '{view}'"
        results = self.con.sql(sql)
        return results["crs"].fetchone()[0]
    
    def view_to_gdf(self, view: str | duckdb.duckdb.DuckDBPyRelation, origin_view : str | None = None, crs : str | None = None):
        if isinstance(view, str):
            crs = self.get_crs(view)
            view = self.con.sql(f"SELECT * FROM {view}")
            
        else:
            if origin_view:
                try: 
                    crs = self.get_crs(origin_view)
                except:
                    crs = None
        
        tmp_view_name = "tmp_" + str(uuid.uuid4()).split("-")[0]
        view.create_view(tmp_view_name)
        sql = f"SELECT * EXCLUDE (geometry), ST_AsText(geometry) as geometry_wkt FROM {tmp_view_name}"
        df = self.con.sql(sql).df()
        df["geometry"] = gpd.GeoSeries.from_wkt(df["geometry_wkt"])
        df.drop(columns=["geometry_wkt"], inplace=True)
        self.con.sql(f"DROP VIEW {tmp_view_name}")
        
        return gpd.GeoDataFrame(df, geometry="geometry", crs=crs)
    
    def sql_with_retries(self, sql, retries=3):
        return sql_with_retries(self.con, sql, retries)
