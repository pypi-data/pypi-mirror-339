"""
This module provides functionality for exporting vector data to PMTiles format.

The module follows a layered architecture:

1. High-level functions:
   - export_gdf_to_pmtiles: Convert a GeoDataFrame directly to PMTiles

2. Core functionality:
   - run_tippecanoe: Run tippecanoe on GeoJSON files to create PMTiles
   - _run_subprocess_with_output: Utility for running subprocesses with output capture

3. Configuration:
   - TileLayerConfig: Configuration class for PMTiles layer settings and operations

The typical workflow is:
1. Data is loaded into DuckDB (either from GeoDataFrame or existing view)
2. Data is exported to GeoJSON (intermediate format)
3. tippecanoe is run on the GeoJSON to create PMTiles
4. The PMTiles file is moved to its final destination (local or S3)
"""

import logging
import subprocess
import geopandas as gpd
import sys
import threading
import io
from .geoduck import GeoDuck2
from pathlib import Path
import tempfile
from .storage import move_file_to_destination
import duckdb
import uuid
from dataclasses import dataclass
import copy
import os
import json

logger = logging.getLogger(__name__)    

class TileLayerConfig:
    """Configuration for a PMTiles layer."""

    def __init__(self, name: str, min_zoom: int = None, max_zoom: int = None):
        """
        Initialize a layer configuration.

        Args:
            name: Name of the layer
            min_zoom: Minimum zoom level for the layer
            max_zoom: Maximum zoom level for the layer
        """
        self.name = name
        self.min_zoom = min_zoom
        self.max_zoom = max_zoom

    def get_tippecanoe_args(self, geojson_path: str) -> list[str]:
        """
        Get tippecanoe arguments for this layer.

        Args:
            geojson_path: Path to the GeoJSON file for this layer

        Returns:
            List of tippecanoe arguments for this layer
        """
        layer_opts = []
        if self.min_zoom is not None:
            layer_opts.append(f"minimum_zoom={self.min_zoom}")
        if self.max_zoom is not None:
            layer_opts.append(f"maximum_zoom={self.max_zoom}")

        layer_arg = f"{self.name}:{geojson_path}"
        if layer_opts:
            layer_arg += f":{','.join(layer_opts)}"

        return ["-L", layer_arg]


@dataclass
class TileOpts:
    opts = []
    
    def __post_init__(self):
        if self.opts is None:
            self.opts = [
                "-zg",
                "--drop-densest-as-needed",
                "--force"
            ]


@dataclass
class TippecanoeLayerConfig:
    args: dict = None
    name: str | None = None
    source: str | None = None

    def __post_init__(self):
        if self.args is None:
            # TODO this currently doesn't support per-layer attributes particularly well
            self.args = dict()
    
    def get_args(self, geojson_path: str | None = None, name: str | None = None):
        name = name or self.name
        geojson_path = geojson_path or self.source

        if name is None:
            raise ValueError("name must be provided")
        
        if geojson_path is None:
            raise ValueError("geojson_path must be provided")

        layer_opts = []
        for arg, value in self.args.items():
            if value is not None:
                layer_opts.append(f"{arg}={value}")
            else:
                layer_opts.append(arg)

        layer_arg = f"{name}:{geojson_path}"
        if layer_opts:
            layer_arg += f":{','.join(layer_opts)}"
        
        return ["-L", layer_arg]

@dataclass
class TippecanoeGeoJSONConfig:
    layers: list[TippecanoeLayerConfig] | TippecanoeLayerConfig
    name_source_pairs: list[tuple[str, str]] | None = None
    
    def __post_init__(self):
        if isinstance(self.layers, list):
            self.layers = self.layers
        elif isinstance(self.layers, TippecanoeLayerConfig):
            if self.name_source_pairs is not None:
                layers_list = []
                for name, source in self.name_source_pairs:
                    lc = copy.deepcopy(self.layers)
                    lc.name = name
                    lc.source = source
                    layers_list.append(lc)
                self.layers = layers_list
            else:
                raise ValueError("layers must be a list of TippecanoeLayerConfig or a TippecanoeLayerConfig")
        else:
            raise ValueError("layers must be a list of TippecanoeLayerConfig or a TippecanoeLayerConfig")
        
    def get_args(self):
        args = []
        for layer in self.layers:
            args.extend(layer.get_args())
        return args
    

class Exporter:
    def __init__(self, geoduck: GeoDuck2):
        self.geoduck = geoduck
    
    def write_geojson(
        self, 
        view: str | duckdb.duckdb.DuckDBPyRelation, 
        path: str = tempfile.NamedTemporaryFile(suffix=".geojson").name) -> str:
        """
        Export a DuckDB view/table to GeoJSON.

        Args:
            view: Name of the view/table to export
            path: Path to write the GeoJSON file

        Returns:
            Path to the created GeoJSON file

        Raises:
            ValueError: If path is None or doesn't end with .geojson
        """
        if path is None:
            raise ValueError("path must be provided")

        if not path.endswith(".geojson"):
            raise ValueError("path must end with .geojson")
        
        drop = False
        if isinstance(view, duckdb.duckdb.DuckDBPyRelation):
            drop = True
            tmp_view_name = "tmp_" + str(uuid.uuid4()).split("-")[0]
            view.create_view(tmp_view_name)
            view = tmp_view_name

        logger.info(f"Exporting layer {view} to GeoJSON")
        sql = f"""
            COPY {view} TO '{path}'
            WITH (FORMAT GDAL, DRIVER 'GeoJSON', LAYER_CREATION_OPTIONS 'WRITE_BBOX=YES')
            """
        self.geoduck.con.sql(sql)

        if drop:
            logger.info(f"Dropping temporary table for layer {view}")
            self.geoduck.con.sql(f"DROP VIEW {view}")

        return path
    
    
    def write_pmtiles_gdal(
        self, 
        view: str | duckdb.duckdb.DuckDBPyRelation, 
        path: str = tempfile.NamedTemporaryFile(suffix=".pmtiles").name) -> str:
        """
        Export a DuckDB view/table to PMTiles using GDAL.

        Args:
            view: View/table to export.  Can be a name or a duckdb.DuckDBPyRelation object.
            path: Path to write the PMTiles file

        Returns:
            Path to the created PMTiles file

        Raises:
            ValueError: If path is None or doesn't end with .pmtiles
            
        This is quite a bit simpler than the Tippecanoe approach as of now, and doesn't support a lot of options.
        """

        if not path.endswith(".pmtiles"):
            raise ValueError("path must end with .pmtiles")
        
        drop = False
        if isinstance(view, duckdb.duckdb.DuckDBPyRelation):
            drop = True
            tmp_view_name = "tmp_" + str(uuid.uuid4()).split("-")[0]
            view.create_view(tmp_view_name)
            view = tmp_view_name

        logger.info(f"Exporting layer {view} to PMTiles")
        sql = f"""
            COPY {view} TO '{path}'
            WITH (FORMAT GDAL, DRIVER 'PMTiles', LAYER_CREATION_OPTIONS 'WRITE_BBOX=YES')
            """
        self.geoduck.con.sql(sql)

        if drop:
            logger.info(f"Dropping temporary table for layer {view}")
            self.geoduck.con.sql(f"DROP VIEW {view}")

        return path
            
    def run_tippecanoe(
        self,
        output_path: str,
        views: list[str | duckdb.duckdb.DuckDBPyRelation] | None = None,
        inputs: TippecanoeGeoJSONConfig | None = None,
        baseConfig: TippecanoeLayerConfig | None = None,
        layerNames: list[str] | None = None,
        tile_opts: TileOpts = TileOpts()
    ):
        """
        Export the current view to a PMTiles file.

        Args:
            output_path: Path to write the PMTiles file
            views: List of views to export (string names or duckdb.DuckDBPyRelation objects)
            inputs: TippecanoeGeoJSONConfig object
            baseConfig: TippecanoeLayerConfig object
            layerNames: List of layer names
            tile_opts: Additional options to pass to tippecanoe (default: ["-zg"])
            
        There's essentially two options:
        1. Provide a list of views and layer names
        2. Provide an inputs object, which contains pre-exported GeoJSON files and layer names
        """
        if views is None and inputs is None:
            raise ValueError("Either view or views must be provided")
        
        if views is not None and inputs is not None:
            raise ValueError("Either views or inputs must be provided, not both")
        
        if inputs is not None:
            args = inputs.get_args()
            
        else: 
            if len(views) == 0:
                raise ValueError("views must be provided as a list of strings or duckdb.DuckDBPyRelation objects")
            
            n_relations = len([i for i in views if isinstance(i, duckdb.DuckDBPyRelation)])
            n_names = len(layerNames)
            
            if n_relations != n_names:
                raise ValueError("layerNames must be provided if views contains duckdb.DuckDBPyRelation objects, and lengths must match")
            
            if baseConfig is None:
                baseConfig = TippecanoeLayerConfig()
            
            args = []
            i_relation = 0
            for view in views:
                if isinstance(view, duckdb.duckdb.DuckDBPyRelation):
                    name = layerNames[i_relation]
                    i_relation += 1
                else:
                    name = view

                geojson_path = self.write_geojson(view)
                lc = copy.deepcopy(baseConfig)
                lc.name = name
                lc.source = geojson_path
                args.extend(lc.get_args())

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            local_output = temp_path / "output.pmtiles"
            # Run tippecanoe to create PMTiles
            cmd = ["tippecanoe"] + args + ["-o", str(local_output)] + tile_opts.opts
            _run_subprocess_with_output(cmd)

            # Move the output file to its destination
            move_file_to_destination(str(local_output), output_path)

        return self


def _run_subprocess_with_output(cmd: list[str]) -> tuple[str, str]:
    """
    Run a subprocess and capture its output using threads.

    Args:
        cmd: Command to run as a list of strings

    Returns:
        Tuple of (stdout_text, stderr_text)

    Raises:
        subprocess.CalledProcessError: If the process returns a non-zero exit code
    """
    stdout_buffer = io.StringIO()
    stderr_buffer = io.StringIO()

    def handle_output(stream, buffer, is_stderr=False):
        for line in iter(stream.readline, ""):
            if not line:
                break
            # Print to appropriate stream
            if is_stderr:
                print(line, end="", file=sys.stderr, flush=True)
            else:
                print(line, end="", flush=True)
            # Store in buffer
            buffer.write(line)

    logger.info(f"Running command: {' '.join(cmd)}")
    # Start the process
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
    )

    # Create threads to handle stdout and stderr simultaneously
    stdout_thread = threading.Thread(
        target=handle_output, args=(process.stdout, stdout_buffer)
    )
    stderr_thread = threading.Thread(
        target=handle_output, args=(process.stderr, stderr_buffer, True)
    )

    # Start threads
    stdout_thread.start()
    stderr_thread.start()

    try:
        # Wait for process to complete
        return_code = process.wait()

        if return_code != 0:
            # Wait for output threads to complete
            stdout_thread.join()
            stderr_thread.join()

            # Get the complete output
            stdout_text = stdout_buffer.getvalue()
            stderr_text = stderr_buffer.getvalue()
            print(stdout_text)
            print(stderr_text)
            raise subprocess.CalledProcessError(
                return_code, cmd, stdout_text, stderr_text
            )
    except Exception:
        # Ensure process is terminated if an exception occurs
        process.terminate()
        raise
    finally:
        # Always wait for threads to complete, regardless of success or failure
        stdout_thread.join()
        stderr_thread.join()

    return stdout_buffer.getvalue(), stderr_buffer.getvalue()