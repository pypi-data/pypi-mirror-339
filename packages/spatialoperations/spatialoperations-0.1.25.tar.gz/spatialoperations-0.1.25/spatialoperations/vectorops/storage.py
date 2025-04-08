import duckdb
import geopandas as gpd
from .utils import register_gdf_to_duckdb, authenticate_duckdb_connection
import s3fs
from tqdm import tqdm
import logging
import copy
import os
import shutil
from urllib.parse import urlparse
from .utils import dummy_tqdm

logger = logging.getLogger(__name__)


def dummy_tqdm(x, *args, **kwargs):
    return x

def _write_parquet_with_metadata(
    con, source_name: str, path: str, partition_by: list[str] = None
):
    """
    Core functionality for writing data to parquet with GeoParquet metadata.

    Args:
        con: DuckDB connection
        source_name: Name of the table/view to write
        path: Path to write the parquet file(s)
        partition_by: Optional list of columns to partition the data by
    """
    # Calculate bbox for Hilbert index
    bbox = con.sql(
        f"""
        SELECT ST_XMin(ST_Extent(geometry)) as xmin,
               ST_YMin(ST_Extent(geometry)) as ymin,
               ST_XMax(ST_Extent(geometry)) as xmax,
               ST_YMax(ST_Extent(geometry)) as ymax
        FROM {source_name}
        """
    ).fetchone()

    # Base COPY options with proper quoting
    copy_options = {"FORMAT": "'PARQUET'", "COMPRESSION": "'ZSTD'"}
    if "s3://" not in path:
        copy_options["OVERWRITE"] = "TRUE"
        authenticate_duckdb_connection(con)

    # Add partition options if specified
    if partition_by:
        partition_cols = ", ".join(partition_by)
        copy_options.update(
            {"PARTITION_BY": f"({partition_cols})", "FILENAME_PATTERN": "'data_{uuid}'"}
        )

    # Convert options to SQL string
    options_str = ", ".join(f"{k} {v}" for k, v in copy_options.items())

    # Note: this + the bbox calculation is slow
    # TODO: give option to avoid it
    # Sort by Hilbert index to improve query performance
    # https://medium.com/radiant-earth-insights/using-duckdbs-hilbert-function-with-geop-8ebc9137fb8a
    con.sql(
        f"""
        COPY (
            SELECT * FROM {source_name}
            ORDER BY ST_Hilbert(
                geometry,
                ST_Extent(
                    ST_MakeEnvelope(
                        {bbox[0]}, {bbox[1]},
                        {bbox[2]}, {bbox[3]}
                    )
                )
            )
        )
        TO '{path}'
        ({options_str})
        """
    )


def write_view_to_parquet(con, view: str, path: str, partition_by: list[str] = None):
    """
    Write a DuckDB view/table to (partitioned) parquet with GeoParquet metadata.

    Args:
        con: DuckDB connection
        view: Name of the view/table to write
        path: Path to write the parquet file(s)
        partition_by: Optional list of columns to partition the data by
    """
    _write_parquet_with_metadata(con, view, path, partition_by)

    
def upload_to_s3(local_path: str, s3_path: str, options: dict = None) -> None:
    """
    Upload a file to S3 using s3fs for all file types.

    Args:
        local_path: Path to the local file to upload
        s3_path: S3 destination path (e.g., 's3://bucket/path/to/file')
        options: Optional dictionary of options:
            - 'content_type': Content type for the file (e.g., 'application/octet-stream')
            - 'metadata': Dict of metadata to attach to the file
            - 'acl': Access control for the file (e.g., 'public-read')
            - Any other options supported by s3fs.put_file

    Example:
        upload_to_s3('local/file.pmtiles', 's3://bucket/path/file.pmtiles')
        upload_to_s3('local/data.parquet', 's3://bucket/data/data.parquet',
                    {'content_type': 'application/parquet'})
    """

    # Check if file exists
    if not os.path.exists(local_path):
        raise FileNotFoundError(f"Local file not found: {local_path}")

    # Parse S3 path
    parsed_url = urlparse(s3_path)
    bucket_name = parsed_url.netloc
    key = parsed_url.path.lstrip("/")

    # If key ends with '/', append the filename from local_path
    if key.endswith("/"):
        key = key + os.path.basename(local_path)

    # Full S3 path without the s3:// prefix
    s3_full_path = f"{bucket_name}/{key}"

    # Set default content type based on file extension
    content_type = None
    if local_path.lower().endswith(".pmtiles"):
        content_type = "application/octet-stream"
    elif local_path.lower().endswith(".parquet"):
        content_type = "application/parquet"
    elif local_path.lower().endswith(".geojson"):
        content_type = "application/geo+json"

    # Create s3fs filesystem
    # This will use AWS credentials from environment variables
    fs = s3fs.S3FileSystem()

    # Get file size for progress reporting
    file_size = os.path.getsize(local_path)

    # Prepare extra arguments for the upload
    extra_args = {}
    if options:
        # Extract content_type from options if provided
        if "content_type" in options:
            content_type = options.pop("content_type")

        # Add remaining options to extra_args
        extra_args.update(options)

    # Add content_type to extra_args if set
    if content_type:
        extra_args["ContentType"] = content_type

    logger.info(
        f"Uploading {local_path} to {s3_path} ({file_size / (1024 * 1024):.2f} MB)"
    )

    try:
        # Upload with progress tracking
        uploaded = 0
        chunk_size = 5 * 1024 * 1024  # 5MB chunks

        with open(local_path, "rb") as local_file:
            with fs.open(s3_full_path, "wb", **extra_args) as s3_file:
                while True:
                    chunk = local_file.read(chunk_size)
                    if not chunk:
                        break
                    s3_file.write(chunk)
                    uploaded += len(chunk)
                    percent = (uploaded / file_size) * 100
                    logger.info(
                        f"Progress: {percent:.1f}% ({uploaded / (1024 * 1024):.2f} MB / {file_size / (1024 * 1024):.2f} MB)"
                    )

        logger.info(f"Successfully uploaded {local_path} to {s3_path}")

    except Exception as e:
        raise Exception(f"Failed to upload file: {str(e)}")


def move_file_to_destination(local_path: str, destination_path: str) -> None:
    """
    Move a file to either S3 or local storage, with fallback handling for S3 failures.

    Args:
        local_path: Path to the local file to move
        destination_path: Destination path (can be local or s3:// URL)

    Raises:
        Exception: If S3 upload fails (with fallback information)
    """
    if destination_path.startswith("s3://"):
        logger.info(f"Uploading output to S3: {destination_path}")
        try:
            upload_to_s3(local_path, destination_path)
        except Exception as e:
            logger.error(f"Failed to upload to S3: {e}")
            # Fallback to local path if S3 upload fails
            local_fallback = f"./output_{os.path.basename(destination_path)}"
            logger.info(f"Saving to local fallback path: {local_fallback}")
            shutil.copy(local_path, local_fallback)
            raise Exception(
                f"S3 upload failed. File saved locally to {local_fallback}"
            ) from e
    else:
        output_dir = os.path.dirname(destination_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        logger.info(f"Moving output to: {destination_path}")
        shutil.move(local_path, destination_path)
    
    