import fsspec
import xarray as xr
from loguru import logger as _logger
from contextlib import contextmanager


def open_remote_netcdfs(
    remote_netcdf_file_paths,
    filecache_kwargs={"cache_storage": "../data/tmp/"},
    netcdf_kwargs={},
    progressbar=False,  
    return_paths=True,
):
    """
    Open a list of remote netcdf files using fsspec and xarray.

    Args:
        paths (list, str): list or string of remote file paths can be a glob pattern
            e.g., "s3://bucket/prefix/*.nc"
        cache_storage (str): local cache directory

    Returns:
        xarray.Dataset: the loaded dataset
    """
    if progressbar:
        from tqdm.dask import TqdmCallback as ProgressBar
    else:
        ProgressBar = contextmanager(lambda: (yield))

    logger = _logger.bind(custom="Utils")

    if isinstance(remote_netcdf_file_paths, str):
        assert remote_netcdf_file_paths.startswith(
            "filecache::"
        ), "paths must start with 'filecache::'"
    elif isinstance(remote_netcdf_file_paths, list):
        assert all(
            [f.startswith("filecache::") for f in remote_netcdf_file_paths]
        ), "paths must start with 'filecache::'"

    fs = fsspec.filesystem("filecache", target_protocol="file", **filecache_kwargs)
    logger.info("Getting remote netcdfs from local cache (downloading if necessary)")
    flist_local = fsspec.open_local(
        remote_netcdf_file_paths, filecache=filecache_kwargs
    )
    if return_paths:
        return flist_local
    open_kwargs = (
        dict(
            chunks={},  # ensures dask
            parallel=True,  # parallel loading
            engine="h5netcdf",
        )
        | netcdf_kwargs
    )
    # read the data and load it into memory
    logger.info("Opening files in parallel with xr.open_mfdataset")
    with ProgressBar():
        ds = xr.open_mfdataset(flist_local, **open_kwargs).load()

    # clear the local cache
    cache_size = fs.cache_size() / 1024**2
    fs.clear_cache()
    logger.info(f"Cache cleared ({cache_size:.2f} MB)")

    return ds
