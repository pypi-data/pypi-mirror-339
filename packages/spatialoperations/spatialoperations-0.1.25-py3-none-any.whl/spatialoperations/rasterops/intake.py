from . import compute, rasterops
from enum import Enum
import xarray as xr
import rioxarray as rxr
import logging
import numpy as np
import copy
from typing import Callable
import gc
from odc.geo.geobox import GeoBox, GeoboxTiles
from coastal_resilience_utilities.utils.geo import transform_point
from tqdm import tqdm

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class IntakeMode(Enum):
    CREATE = "create"
    APPEND = "append"


def create_dataset_schema(
    dc: rasterops.DataCube,
    group: str | None = None,
    varnames: list[str] | None = None,
    mode: IntakeMode = IntakeMode.CREATE,
):
    varnames_to_create = varnames if varnames else dc.varnames

    # Standard 2D schema, could be made more flexible
    big_ds = dc.get_data_layout(varnames_to_create)

    # Configure Zarr to preserve NaN values
    zarr_kwargs = {
        "mode": "w" if mode == IntakeMode.CREATE else "a",
        "compute": False,
        "zarr_format": 3,
        "consolidated": False,
        "encoding": {
            k: {
                "dtype": "float32",
                "_FillValue": dc.nodata,
            }
            for k in varnames_to_create
        },
    }
    if mode == IntakeMode.CREATE:
        big_ds.to_zarr(dc.storage.get_storage(), group=group, **zarr_kwargs)

    elif mode == IntakeMode.APPEND:
        big_ds.to_zarr(dc.storage.get_storage(), group=group, **zarr_kwargs)


class Intake:
    def __init__(self, dc: rasterops.DataCube):
        self.dc = dc

    def create_dataset_schema(
        self,
        group: str | None = None,
        varnames: list[str] | None = None,
        mode: IntakeMode = IntakeMode.CREATE,
    ):
        varnames_to_create = varnames if varnames else self.dc.varnames

        # Standard 2D schema, could be made more flexible
        big_ds = self.dc.get_data_layout(varnames_to_create)

        # Configure Zarr to preserve NaN values
        zarr_kwargs = {
            "mode": "w" if mode == IntakeMode.CREATE else "a",
            "compute": False,
            "zarr_format": 3,
            "consolidated": False,
            "encoding": {
                k: {
                    "dtype": "float32",
                    "_FillValue": self.dc.nodata,
                }
                for k in varnames_to_create
            },
        }
        if mode == IntakeMode.CREATE:
            big_ds.to_zarr(self.dc.storage.get_storage(), group=group, **zarr_kwargs)

        elif mode == IntakeMode.APPEND:
            big_ds.to_zarr(self.dc.storage.get_storage(), group=group, **zarr_kwargs)

    def prep_single_tile(
        self, da: xr.DataArray | str, idx: tuple[int, int], boxbuff: int = 0.1
    ):
        logging.getLogger("botocore.credentials").setLevel(logging.WARNING)

        if isinstance(da, str):
            da = rxr.open_rasterio(da).isel(band=0)
        tile = self.dc.tiles[idx]
        bbox = tile.boundingbox
        bl = transform_point(bbox.left, bbox.bottom, self.dc.crs, da.rio.crs)
        tr = transform_point(bbox.right, bbox.top, self.dc.crs, da.rio.crs)

        # Get a dummy data array with the same shape as the tile
        empty_tile_as_da = self.dc.geobox_to_rxr(tile)

        # Clip the data array to the tile in the native CRS of the data array
        # Need to buffer a little bit to avoid edge effects after reprojecting
        # boxbuff = 10000
        try:
            da_clipped = da.rio.clip_box(
                minx=bl.x - boxbuff,
                miny=bl.y - boxbuff,
                maxx=tr.x + boxbuff,
                maxy=tr.y + boxbuff,
            )
            # Now that data is smaller, reproject it to the tile
            da_tiled = da_clipped.rio.reproject(self.dc.crs)
            da_tiled = da_tiled.reindex_like(
                empty_tile_as_da, method="nearest", tolerance=self.dc.dx
            )
            gc.collect()
            return (idx, da_tiled)
        except (
            rxr.exceptions.NoDataInBounds,
            rxr.exceptions.OneDimensionalRaster,
        ) as e:
            print(e)
            return None

    def set_single_tile(
        self, idx: tuple[int, int], da: xr.DataArray, var: str, group: str = None
    ):
        if np.isnan(da).all():
            return None
        else:
            return self.dc.set_data(var, idx, da, group=group)

    def set_tiles(
        self,
        tiles: list[tuple[tuple[int, int], xr.DataArray]],
        var: str,
        group: str = None,
    ):
        compute_items = [compute.Args(args=[idx, da, var, group]) for idx, da in tiles]
        results = self.dc.compute.execute(self.set_single_tile, compute_items)
        if self.dc.store_active_idxs:
            self.dc.storage.store_active_idxs(var, group, results)
        return results

    def da_to_tiles(
        self, da: xr.DataArray | str, idxs: list[tuple[int, int]], boxbuff: int = 0.1
    ):
        compute_items = [compute.Args(args=[da, idx, boxbuff]) for idx in idxs]
        results = self.dc.compute.execute(self.prep_single_tile, compute_items)
        return [r for r in results if r is not None]

    def intake_data(
        self,
        da: xr.DataArray,
        var: str,
        group: str,
        idxs: list[tuple[int, int]] = [],
        boxbuff: int = 0.1,
        batch_size: int | None = 1000,
    ):
        if len(idxs) == 0:
            idxs = list(self.dc.tiles_for_da(da))
        logging.info(f"Tiles for {group}/{var}: {len(idxs)}")

        if batch_size:
            for i in range(0, len(idxs), batch_size):
                batch_idxs = idxs[i : i + batch_size]
                logging.info(
                    f"Processing batch {i // batch_size + 1} with {len(batch_idxs)} tiles"
                )
                tiles = self.da_to_tiles(da, batch_idxs, boxbuff)
                logging.info(
                    f"Setting {len(tiles)} tiles for {group}/{var} in batch {i // batch_size + 1}"
                )
                self.set_tiles(tiles, var, group)
            return None

        else:
            logging.info(f"Intaking {len(idxs)} tiles for {group}/{var}")
            tiles = self.da_to_tiles(da, idxs, boxbuff)
            logging.info(f"Setting {len(tiles)} tiles for {group}/{var}")
            results = self.set_tiles(tiles, var, group)
            return results


def compile(dc, idx, vars, group):
    import warnings

    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore", category=RuntimeWarning, message="All-NaN axis encountered"
        )
        das = [dc.get_single_xarray_tile(var, idx, group=group) for var in vars]
        return das[0].copy(data=np.nanmin([da.data for da in das], axis=0))


def split_data(
    dc: rasterops.DataCube,
    da: xr.DataArray,
    data_split_size: int = 1e5,
    boxbuff: int = 100,
    filter_empty: bool = True,
    show_progress: bool = True,
):
    gb = GeoBox.from_bbox(
        da.rio.bounds(), crs=da.rio.crs, resolution=da.rio.resolution()[0]
    )
    gbt = GeoboxTiles(gb, (data_split_size, data_split_size))
    tiles = list(gbt._all_tiles())

    logging.info(f"Splitting into {len(tiles)} tiles")

    def get_data_by_tile(idx):
        tile = gbt[idx]
        extent = tile.boundingbox
        to_return = da.rio.clip_box(
            minx=extent.left - boxbuff,
            miny=extent.bottom - boxbuff,
            maxx=extent.right + boxbuff,
            maxy=extent.top + boxbuff,
        )
        to_return.rio.write_crs(da.rio.crs, inplace=True)
        to_return.rio.write_nodata(da.rio.nodata, inplace=True)
        to_return = to_return.where(to_return != to_return.rio.nodata)
        gc.collect()
        if np.isnan(to_return.data).all():
            return None
        else:
            return to_return

    compute_items = [compute.Args(args=[idx]) for idx in tiles]
    results = dc.compute.execute(get_data_by_tile, compute_items)
    return results


def multi_intake(
    dc: rasterops.DataCube,
    data: dict[str, xr.DataArray],
    group: str,
    idxs: list[tuple[int, int]] = [],
    show_progress: bool = True,
    compile=True,
    output_var: str = None,
    output_group: str = None,
    compile_function: Callable = compile,
    mode: IntakeMode = IntakeMode.APPEND,
):
    logging.info(
        f"Creating dataset schema for {list(set(list(data.keys()) + [output_var]))}"
    )
    dc.intake.create_dataset_schema(
        group=group, varnames=list(set(list(data.keys()) + [output_var])), mode=mode
    )
    logging.info("Dataset schema created")

    def loop(var, data):
        dc.intake.intake_data(data, var, group, idxs=idxs)
        gc.collect()

    if show_progress:
        from tqdm import tqdm

        for var, da in tqdm(data.items(), position=0):
            loop(var, da)
    else:
        for var, da in data.items():
            loop(var, da)

    if compile:
        if len(idxs) == 0:
            idxs = dc.storage.get_multi_active_idxs(list(data.keys()), group)

        compute_items = [
            compute.Args(args=[dc, idx, list(data.keys()), group]) for idx in idxs
        ]
        results = dc.compute.execute(compile_function, compute_items)
        if output_var:
            if output_group is None:
                output_group = group
            dc.intake.set_tiles(zip(idxs, results), var=output_var, group=output_group)
