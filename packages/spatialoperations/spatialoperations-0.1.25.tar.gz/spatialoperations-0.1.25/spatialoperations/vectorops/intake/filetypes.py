import enum
import geopandas as gpd
import pandas as pd
class DataType(enum.Enum):
    """
    Enum of accepted data types for spatial data operations.
    """
    PARQUET = "parquet"
    GEOPACKAGE = "gpkg"
    GEOJSON = "geojson"
    SHAPEFILE = "shp"
    CSV = "csv"
    GDF = "gdf"
    
    @classmethod
    def from_extension(cls, file_path: str):
        """
        Get the file type from a file path extension.
        
        Args:
            file_path: Path to the file
            
        Returns:
            FileType enum value
        
        Raises:
            ValueError: If the file extension is not supported
        """
        if isinstance(file_path, gpd.GeoDataFrame) or isinstance(file_path, pd.DataFrame):
            return cls.GDF
        
        extension = file_path.split(".")[-1].lower()
        for file_type in cls:
            if extension == file_type.value:
                return file_type
        raise ValueError(f"Unsupported file extension: {extension}")
    
    @classmethod
    def is_supported(cls, file_path: str) -> bool:
        """
        Check if a file type is supported based on its extension.
        
        Args:
            file_path: Path to the file
            
        Returns:
            True if the file type is supported, False otherwise
        """
        try:
            cls.from_extension(file_path)
            return True
        except ValueError:
            return False
        
    
    @classmethod
    def get_loader_function(cls, file_type):
        """
        Get the appropriate loader function for a given file type.
        
        Args:
            file_type: FileType enum value
            
        Returns:
            Function to load the specified file type
            
        Raises:
            ValueError: If the file type does not have a supported loader
        """
        from .intake import ogr_to_parquet, gdf_to_parquet
        
        LOADERS = {
            cls.GEOPACKAGE: ogr_to_parquet,
            # Add more loaders as they become available
            cls.SHAPEFILE: ogr_to_parquet,
            cls.GDF: gdf_to_parquet,
            # cls.GEOJSON: geojson_loader_function,
            # cls.CSV: csv_loader_function,
        }
        
        if file_type not in LOADERS:
            raise ValueError(f"No loader available for file type: {file_type.value}")
        
        return LOADERS[file_type]
