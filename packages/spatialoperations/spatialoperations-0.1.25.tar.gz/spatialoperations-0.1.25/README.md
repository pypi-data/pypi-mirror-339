# SpatialOperations

This repo leverages cloud-native-geospatial tooling alongside Kubernetes and S3 infrastructure (currently geared around NRP Nautilus), to create high-performance spatial workflows.

It is designed to:
1. Publish the `spatialoperations` package, which supports operations around cloud-native raster and vector operations
2. Abstract compute and storage, so that high-throughput computing like dask can run on cloud-native data
3. Deploy a jupyter notebook for analysis
4. Manage exports and APIs for visualizing and sharing data.  Via Rest APIs, COGs, and PMTiles.

## Distribution
The package is distributed using PyPI, and built/published using UV.  It is intended to be installed via conda, which does a good job of managing GDAL as a dependency.

In the future we'll build a conda recipe that manages this better, but currently installing via conda + pip has been effective.  Examples of installation can be found in the environments yaml files.

## Environments

The `environments` directory contains the base environment and any other environments that are needed.

The `base` environment is the core dependencies for all later tooling and environments.

## Publishing Base Environment

### Setting up the `config.mk`
See the example `config.mk`.  This is expected to export two paths at the moment, `VOLUME_MOUNTS` and `ENV_FILES`.  The rest is just to construct these variables.

### Adding a new dependency

When adding a new dependency to the project:

1. Add the package to `pyproject.toml`:
```toml
dependencies = [
    "new-package>=1.0.0",
]
```

2. Update the package version:
```toml
[project]
name = "spatialoperations"
version = "0.1.1"
```

### Publishing the base environment to PyPI
This requires a `UV_PUBLISH_TOKEN` in `.env.publish`
3. Build the base environment:
```bash
# Build and run the container
make publisher-build
make publisher-run

# Publish to PyPI
make publish
```

This publishes the `spatialoperations` package to PyPI.

## Building downstream environments
We use a two-stage build:
1. `analysis`, which builds a base image that has everything we need, particularly:
  - `spatialoperations`, installed from PyPI
  - `pmtiles`
2. `jupyter`, which includes the jupyter-specific dependencies.  This relies on the `analysis` base image.

These can be created with `make analysis-build` and `make jupyter-build`, and run with `make analysis-run` and `make jupyter-run`.


### Example rasterops environment
```yaml
name: rasterops
channels:
  - conda-forge
dependencies:
  - python>=3.12.0,<3.13.0
  - gdal>=3.10.0
  - pip:
    - geospatial-analysis-environment>=0.1.9
    - coastal_resilience_utilities>=0.1.35
```

## Building the analysis environment

1. Update any dependencies in `environments/analysis/analysis.yml`

2. Build the analysis environment:
```bash
make analysis-build
make analysis-run
```

## Building the jupyter environment

1. Update any dependencies in `environments/jupyter/jupyter.yml`

2. Build the jupyter environment:
```bash
make jupyter-build
make jupyter-run
```


## Prerequisites

1. Install `helm` (On MacOSX):
```bash
brew install helm
```
See https://helm.sh/docs/intro/install/ for other systems.

2. Configure AWS credentials:
Create a file named `.env.s3` with your Nautilus Cept S3 credentials.  See `.env.s3.example`, as their may be other variables needed.

## Deployment

Create a deployment with a pod, ingress, and persistent volume unique to you:
```bash
make jupyter-push
make jupyter-deploy
```

Release resources when you're done:
```bash
make jupyter-teardown
```

## Formatting

You can use [ruff](https://docs.astral.sh/ruff/formatter/#ruff-format) to
format your code before committing. The easiest way is to make sure that `uv`
is installed and run `make format`. If you want to make sure that files are
formatted as you save them make sure to install the relevant `ruff` extension
(https://marketplace.cursorapi.com/items?itemName=charliermarsh.ruff for
VSCode/Cursor).

## Developing Dependencies on a deployed Jupyter server

You will need to have `fswatch` installed (`brew install fswatch`). To develop
`spatialoperations` just run:

```
make dev-spatialoperations
```

This command will ensure that there is a server running at
`https://dev-jupyter.nrp-nautilus.io`.

Don't forget to use `importlib` to reload dependencies from disk:

```
import importlib
import rasterops

# If you change a file locally, wait for it to be synced and then run:

importlib.reload(rasterops)

```

If you want to make sure that the dev server is shut down you can just run

```
helm uninstall dev
```
