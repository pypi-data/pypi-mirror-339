import pytest


def test_import_gdal():
    from osgeo import gdal

    assert True


def test_import_xarray():
    import xarray

    assert True


def test_import_geopandas():
    import geopandas

    assert True


def test_import_spatialops():
    import spatialoperations.rasterops
    import spatialoperations.vectorops

    assert True
