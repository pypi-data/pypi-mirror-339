"""
A script to download ERA5 data from Google's Weatherbench dataset.

Usage
-----
```
fetcher = era5fetcher.ERA5CryoGridForcingFetcher(
    # standard BBOX format: [West, South, East, North]
    bbox_WSEN=(43, 58, 90, 24),
    # time will be replaced with values when calling fetcher.fetch(time=t)
    dest_path='./data/era5-cryogrid_forcing-{time:%Y%m%d}.nc',
)

# fetches and downloads the given time step
ds = fetcher.fetch(time='2024-01-06')

# if called again, will load saved file instead of downloading the data again
```

Dependencies
------------
```text
python>=3.10
dask
fsspec
h5netcdf
loguru
pandas
scipy
tqdm
xarray

Other info
----------
Created by Luke Gregor / gregorl@ethz.ch
"""

import fsspec
import pathlib
import xarray as xr
import pandas as pd
from loguru import logger
from typing import Union, Literal
from tenacity import retry, stop_after_attempt, after_log
import tempfile
import dotenv
import atexit
from functools import singledispatchmethod, lru_cache


RETRY_KWARGS = dict(
    stop=stop_after_attempt(3),
    after=after_log(logger.bind(class_name="Retry"), "WARNING"),
    reraise=True,
)


class ERA5GoogleCloudNetCDFFetcher:
    """Base class to download netCDF data from the Google Cloud's dataset.

    For downloading data, see ERA5CryoGridForcingFetcher class
    """

    def __init__(
        self,
        bbox: Union[tuple, list],
        levels: Union[tuple, list, None],
        variables: Union[tuple, list],
        time_steps: tuple = (0, 3, 6, 9, 12, 15, 18, 21),
        logging_level: Literal["TRACE", "DEBUG", "INFO", "SUCCESS", "WARNING"] = "INFO",
        cache_dir="./era5_downloader_tmp/",
        mkdtemp=True,
        **kwargs,
    ):
        """
        Fetches ERA5 data from Google Cloud Storage and returns an xarray dataset.

        Args:
            bbox (tuple): (lon_min, lat_min, lon_max, lat_max)
            levels (list): pressure levels to retrieve.
            variables (list): variables to retrieve
            time_steps (tuple): hour time steps to retrieve. Default is every 3rd hour.
            n_threads (int): number of threads to use (default 8). Speed limited by bandwidth.
            progressbar (bool): show progress bar
            cache_dir (str): path to store cache (can get quite big)
            mkdtemp (bool): add a folder with name {timestamp}_{hash} to use as cache
            logging_level (str): logging level for loguru logger [TRACE, DEBUG, INFO, SUCCESS, WARNING]
            kwargs: additional keyword arguments that are not used in this class
        """
        self.logger = self._make_logger(logging_level=logging_level)

        if dotenv.load_dotenv():
            self.logger.success(f"Loaded .env file from {dotenv.find_dotenv()}")

        self.uri_levels = "filecache::gs://gcp-public-data-arco-era5/raw/date-variable-pressure_level/{t:%Y}/{t:%m}/{t:%d}/{variable}/{level}.nc"
        self.uri_surface = "filecache::gs://gcp-public-data-arco-era5/raw/date-variable-single_level/{t:%Y}/{t:%m}/{t:%d}/{variable}/surface.nc"

        self.tmp_dir = self._create_tmp_dir(cache_dir, mkdtemp=mkdtemp)
        self.fs_remote = fsspec.filesystem("gs", token="anon")
        self.fs_cache = fsspec.filesystem(
            "filecache", target_protocol="file", cache_storage=str(self.tmp_dir)
        )

        self._set_valid_variable_list()  # stored in self._valid_surface_vars and self._valid_level_vars
        self.levels = self._check_levels(levels)
        self.bbox = self._prep_bbox(bbox)
        self.variables = tuple(variables)
        self.time_steps = time_steps

        # hidden features that can be used for testing
        self._clear_cache_after_download = True
        self._spacing = 4  # for pretty printing

        # will delete cache on exit - must remove any files and then remove the directory
        atexit.register(self.clear_cache)

    ## functions used on initialisation
    def _make_logger(self, logging_level="INFO"):
        import sys

        logger_fmt = (
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}.{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        )

        logger.remove()
        logger.add(sys.stdout, level=logging_level, format=logger_fmt)

        return logger.bind(custom=self.__class__.__name__)

    def _create_tmp_dir(self, tmp_base, mkdtemp=True):
        tmp_base = pathlib.Path(tmp_base).expanduser().resolve()
        tmp_base.mkdir(parents=True, exist_ok=True)

        if mkdtemp:
            now = pd.Timestamp.now().strftime("%Y%m%d%H%M%S_")
            tmp_dir = tempfile.mkdtemp(dir=str(tmp_base), prefix=now)
            self.logger.debug(
                f"Using cache directory (with newly created subfolder):  {tmp_dir}"
            )
        else:
            self.logger.warning(
                "All files and folders in the cache directory will be removed after each download. "
                "This may cause issues if you are running several download instances with the same "
                "cache directory."
            )
            tmp_dir = tmp_base
            flist = list(tmp_dir.iterdir())
            if len(flist) > 0:
                tmp_dir_size = sum(f.stat().st_size for f in flist) / 1024**2
                self.logger.warning(
                    f"Cache directory contains {len(flist)} files/folders ({tmp_dir_size:.2f} MB) - will be removed on completion"
                )

        return tmp_dir

    def _set_valid_variable_list(self):
        """
        Fetches the available variables from Google Store.
        Only run on initialization.

        Sets:
            self._valid_surface_vars (list): list of surface variables
            self._valid_level_vars (list): list of level variables
        """
        self.logger.debug("Getting list of valid variables")

        def drop_n_levels_in_uri(uri, n=2):
            uri = uri.replace("filecache::", "").replace("gs://", "")
            return "/".join(uri.split("/")[:-n])

        def get_name(f):
            return f.split("/")[-1].replace(".nc", "")

        fs = self.fs_remote

        t = pd.Timestamp("2000-01-01")
        uri_surface_vars = drop_n_levels_in_uri(self.uri_surface).format(t=t)
        uri_levels_vars = drop_n_levels_in_uri(self.uri_levels).format(t=t)
        uri_level_values = drop_n_levels_in_uri(self.uri_levels, n=1).format(
            t=t, variable="temperature"
        )

        self._valid_surface_vars = [get_name(f) for f in fs.ls(uri_surface_vars)]
        self._valid_level_vars = [get_name(f) for f in fs.ls(uri_levels_vars)]
        self._valid_levels = [int(get_name(f)) for f in fs.ls(uri_level_values)]
        self.logger.debug(
            "Set valid variables and levels to: ._valid_surface_vars, ._valid_level_vars, ._valid_levels"
        )

        self.logger.trace(f"Valid surface variables: {self._valid_surface_vars}")
        self.logger.trace(f"Valid pressure level variables: {self._valid_level_vars}")
        self.logger.trace(f"Valid pressure levels: {self._valid_levels}")

    def _check_levels(self, levels):
        """
        Check if given levels are available in the ERA5 dataset.

        Args:
            levels (list): pressure levels to retrieve

        Returns:
            levels (list): pressure levels to retrieve

        Raises:
            ValueError: if level is not available
        """
        if levels is None:
            self.logger.debug(
                "You have not provided levels. Will be in surface mode only"
            )
            return []
        for level in levels:
            if level not in self._valid_levels:
                raise ValueError(
                    f"Level {level} not available. "
                    f"Available levels are: {self._valid_levels}"
                )

        return levels

    def _prep_bbox(self, bbox):
        """
        ERA5 data is stored in 0:360 format, so we need to convert -180:180 to 0:360
        """
        w, s, e, n = bbox
        if (w < 0) or (e < 0):
            self.logger.debug("BBOX: Converting -180:180 longitudes to 0:360")
            w = w % 360
            e = e % 360
            if w == 180 and e == 180:
                w, e = 0, 360
        if w > e:
            self.logger.warning(f"BBox-west > BBox-east : {w} > {e}, swapping")
            w, e = e, w
        if s > n:
            self.logger.warning(f"BBox-south > BBox-north : {s} > {n}, swapping")
            s, n = n, s
        self.logger.debug(f"Bounding box for ERA5 data [W, S, E, N]: {w, s, e, n}")
        return w, s, e, n

    ## methods usable by the user
    def get_raw(self, time: pd.Timestamp):
        """
        High level function to download data for a specific time
        and return it as an xarray dataset.

        Data are downloaded to a cache folder that is cleared on completion

        Args:
            time (pd.Timestamp): day to download (hours not supported)
            storage_options (dict): options for fsspec

        Returns:
            ds (xr.Dataset): downloaded dataset subsetted to bbox and time slice
        """
        time = pd.Timestamp(time)
        self.logger.info(f"Getting data for {time:%Y-%m-%d}")

        # get the list of URIs to download
        uris = list(self.make_uri_list(time))
        # download the files concurrently - mostly limited by network
        flist = self._retrieve_with_fsspec(uris)  # also sets _fsspec_cache (dict)

        # open the files and preprocess
        self.logger.debug(f"Opening and preprocessing the {len(flist)} files")
        ds = xr.open_mfdataset(
            flist,
            chunks={},  # ensures dask
            parallel=True,  # parallel loading
            preprocess=self._netcdf_preprocessor,
            engine="scipy",
        ).load()

        # clear the cache
        if self._clear_cache_after_download:
            self.clear_cache(remove_folder=False)
        else:
            self.logger.warning("Cache not cleared, will use up a lot of disk space")

        return ds

    def make_uri_list(self, t: pd.Timestamp):
        """
        Generates URIs for each variable and level combination for a given time.

        Args:
            t (pd.Timestamp): time for which to generate URIs

        Yields:
            uri (str): URI to download data from
        """
        for variable in self.variables:
            # will return 'surface', 'level', or 'both'
            surface_or_level = self._surface_or_level_variable(variable)
            if surface_or_level == "surface":
                yield self._build_single_uri(t, variable)
            elif surface_or_level == "level":
                for level in self.levels:
                    yield self._build_single_uri(t, variable, level)
            elif surface_or_level == "both":
                # if both, we download the surface variable and the level variable
                # surface variables are renamed with _surface suffix in the
                # get_netcdf_dataset function to avoid conflicts with the level variables
                yield self._build_single_uri(t, variable)
                for level in self.levels:
                    yield self._build_single_uri(t, variable, level)

    def clear_cache(self, remove_folder=True):
        """Clears the cache directory"""

        # precleaning the cache
        cache_mb = self.fs_cache.cache_size() / 1024**2
        self.logger.debug(f"Clearing fsspec.fs_cache and freeing {cache_mb:.2f} MB")
        self.fs_cache.clear_cache()

        if remove_folder:
            self.logger.debug(f"Removing cache directory {self.tmp_dir}")
            tmp_dir = pathlib.Path(self.tmp_dir)
            # remove all files in the directory
            [f.unlink() for f in tmp_dir.iterdir() if f.is_file()]
            # remove the directory if it is empty
            tmp_dir.rmdir()

    ## hidden functions that are called by the unprotected methods
    def _retrieve_with_fsspec(self, uri_list: list) -> list:
        """Downloads files locally using fsspec and returns local paths

        Also sets the local cache as a property of the class
        """
        self.logger.debug(
            f"Downloading {len(uri_list)} raw ERA5 netCDF files with fsspec to {self.tmp_dir}"
        )
        self.logger.trace(f"URI list: {uri_list}")
        flist = fsspec.open_local(
            uri_list, filecache=dict(cache_storage=str(self.tmp_dir))
        )

        self._set_fsspec_cache(return_key="fn")

        return flist

    def _netcdf_preprocessor(self, ds):
        """
        Preprocess the netcdf dataset after downloading.

        Performs the following operations:
            1. get original uri from fsspec cache (used in 3, 4)
            2. subset the data
            3. renames variables that might clash if it is surface and press_level
            4. expand dimension if pressure level for concat
            5. sets the file name as name_requested attribute
            6. converts to float32 for space saving

        Args:
            ds (xr.Dataset): downloaded dataset

        Returns:
            ds (xr.Dataset): preprocessed dataset
        """
        # things to do here:
        # - rename surface variables that clash with level variables
        # - add level as a coordinate - a bit more tricky
        # - subset to bbox - easy with xarray
        # - subset to time steps
        uri = self._get_original_filename_from_cache(ds)

        request_variable = self._get_variable_name_from_uri(uri)
        # determine if the variable is a surface variable, a level variable, or both
        data_type = self._surface_or_level_variable(
            self._get_variable_name_from_uri(uri)
        )
        # check if a pressure level variable
        is_level = "pressure_level" in uri

        # subset data to bbox and hours
        ds = ds.sel(
            latitude=slice(self.bbox[3], self.bbox[1]),  # north, south
            longitude=slice(self.bbox[0], self.bbox[2]),  # west, east
            time=ds.time.dt.hour.isin(self.time_steps),
        )  # hours

        # sort out variables with same name (e.g. geopotential = z)
        # always assume one variable per file
        key = list(ds.data_vars)[0]
        # surface variables that are also available as pressure levels
        # will be renamed with _surface suffix
        if (data_type == "both") and not is_level:
            ds = ds.rename({key: key + "_surf"})
            key = key + "_surf"

        # pressure_level files do not have a level dimension,
        # so we add it so we can merge them later
        if is_level:
            name_wo_ext = uri.split("/")[-1].replace(".nc", "")
            if not name_wo_ext.isdigit():
                raise ValueError(
                    f"Level file {name_wo_ext} does not have a level in the filename"
                )
            ds = ds.expand_dims(level=[int(name_wo_ext)])

        ds[key].attrs.update({"source": uri, "name_requested": request_variable})

        ds = ds.astype("float32")

        return ds

    def _surface_or_level_variable(self, variable: str):
        """
        Check if a variable is a surface variable, a level variable, or both.

        Args:
            variable (str): variable name

        Returns:
            str: 'surface', 'level', or 'both'
        """
        if variable in self._valid_surface_vars and variable in self._valid_level_vars:
            return "both"
        elif variable in self._valid_surface_vars:
            return "surface"
        elif variable in self._valid_level_vars:
            return "level"
        else:
            raise ValueError(
                f"Variable {variable} not found in either surface or level variables"
            )

    def _build_single_uri(self, t: pd.Timestamp, variable: str, level: int = None):
        """Builds a URI for a single variable and level combination

        Automatically selects the surface or pressure levels URI based on
        if pressure levels are given or not

        Args:
            t (pd.Timestamp): time to download
            variable (str): variable to download
            level (int): pressure level to download

        Returns:
            uri (str): URI to download data from

        Raises:
            KeyError: raised when formatting key in string is not passed
        """
        if level is None:
            uri = self.uri_surface
        else:
            uri = self.uri_levels
        return uri.format(t=t, variable=variable, level=level)

    def _set_fsspec_cache(self, return_key=None):
        """
        Reads the fsspec cache file and returns a dictionary
        """
        import json

        cache_fname = pathlib.Path(self.tmp_dir) / "cache"
        with open(cache_fname, "r") as f:
            cache = json.load(f)

        if return_key is not None:
            cache = {cache[k][return_key]: cache[k] for k in cache}

        self._fsspec_cache = cache

    def _get_original_filename_from_cache(self, ds):
        """Uses the cache to get the original filename"""
        cache = self._fsspec_cache
        fname_hash = pathlib.Path(ds.encoding["source"]).name
        return cache[fname_hash]["original"]

    def _get_variable_name_from_uri(self, uri: str):
        """get the variable name from the URI, assumes just before file name"""
        return uri.split("/")[-2]

    ## dunder methods
    def __repr__(self):
        import pprint

        s = self._spacing * " "

        vars_pretty = pprint.pformat(self.variables)[1:-1].replace(
            "\n", f"\n{(s * 2)[:-1]}"
        )
        vars_pretty = f"(\n{s * 2}{vars_pretty})"  # .replace("'", "")

        text = (
            f"{self.__class__.__name__}(\n"
            f"{s}bbox = {self.bbox}, \n"
            f"{s}levels = {self.levels}, \n"
            f"{s}variables = {vars_pretty}, \n"
            f"{s}cache_path = '{self.tmp_dir}', \n"
            f"{s}time_steps = {self.time_steps}, \n"
            ")"
        )
        return text

    def __getitem__(self, t):
        assert isinstance(t, (str, pd.Timestamp))
        return self.get_raw(t)

    def __call__(self, t):
        return self.get_raw(t)


class ERA5Downloader(ERA5GoogleCloudNetCDFFetcher):
    """
    Adds the fetch method -- could probably incorporate this into the parent class
    """

    def __init__(
        self,
        bbox_WSEN: tuple,
        region_name: str,
        variables: tuple,
        levels: tuple = None,
        dest_path="../data/era5-{region_name}/{time:%Y}/era5-{region_name}-{time:%Y%m%d}.nc",
        **kwargs,
    ):
        """
        A class to download ERA5 data to force the CryoGrid Community Model.

        Args:
            bbox_WSEN (tuple):
            region_name (str): region_name of the region for file naming purposes
            levels (tuple): levels to download
            variables (tuple): variables to download
            dest_path (str): the output path of the netCDF - use default as example
                can be any fsspec path
        """
        assert "{time:" in dest_path, "dest_path must contain {time:...} placeholder"
        assert dest_path.endswith(".nc"), "dest_path must be a netCDF file"

        self.dest_path = dest_path
        self.region_name = region_name

        self._kwargs = kwargs
        self._kwargs.update(region_name=region_name)

        self.fs_local = fsspec.url_to_fs(dest_path)[0]

        super().__init__(bbox=bbox_WSEN, levels=levels, variables=variables, **kwargs)

        self.logger.info(f"Initialized {self.__class__.__name__} with \n{self}")

    def _make_formatted_dest_path(self, str_path):
        """
        Formats the dest_path string with the kwargs

        Args:
            str_path (str): path to format
        
        Returns:
            str_path (str): formatted path

        Examples:
            >>> self._make_formatted_dest_path("era5-{region_name}/{time:%Y}/era5-{region_name}-{time:%Y%m%d}.nc")
            era5-global/2024/era5-global-20240106.nc
        """
        import re

        str_path = re.sub(r"(\{)(time:)(.*?)(\})", "{{\g<3>}}", str_path)
        str_path = str_path.replace("%Y", "YYYY")
        str_path = str_path.replace("%m", "MM")
        str_path = str_path.replace("%d", "DD")
        str_path = str_path.format(**self._kwargs)

        return str_path
    
    @singledispatchmethod
    @retry(**RETRY_KWARGS)
    def download(self, time, **kwargs):
        """
        Download ERA5 data for a specific time and save it to a netcdf file.

        Calls ERA5WeatherBenchNetCDFFetcher.get(time=time) to fetch the data
        and then saves the returned dataset to the path given when initiating
        the class.

        Args:
            time (str, pd.Timestamp, slice): time to fetch from ERA5 weatherbench netCDF files
            encoding_params (dict): passed as encoding for each variable when writing the
                netcdf file. Defualt is `{complevel: 1, zlib: True, dtype: float32}`

        Returns:
            ds (xr.Dataset): downloaded dataset
        """
        raise NotImplementedError(
            f"Download method not implemented for type {type(time)}"
        )

    @download.register
    @lru_cache(maxsize=10)
    def _(self, time: pd.Timestamp, **kwargs):
        # swap out {time} placeholder
        target_path = str(self.dest_path).format(time=time, **self._kwargs)

        # return existing file if present
        if self.fs_local.exists(target_path):
            self.logger.info(f"File exists: {target_path}")
        else:
            ds = (
                self.get_raw(time)
                .pipe(self._process_before_saving)
                .pipe(self._add_netcdf_attrs)
            )

            # save the netcdf file
            self._to_netcdf(ds, target_path, **kwargs)
            self.logger.success(f"Saved to {target_path}")

        return target_path

    @download.register
    def _(self, time: str, **kwargs):
        time = pd.Timestamp(time)
        return self.download(time, **kwargs)

    @download.register
    def _(self, time: slice, **kwargs):
        assert time.step is None, "Step not supported"
        assert isinstance(
            time.start, (pd.Timestamp, str)
        ), "Start must be a pd.Timestamp or str"
        assert isinstance(
            time.stop, (pd.Timestamp, str)
        ), "Stop must be a pd.Timestamp or str"
        return [
            self.download(t, **kwargs) for t in pd.date_range(time.start, time.stop)
        ]

    def __getattribute__(self, name):
        # thank you ChatGPT for this one

        # Intercept download to check for keyword misuse
        attr = super().__getattribute__(name)

        if ((name == "download") or (name == "fetch_local")) and callable(attr):
            def wrapper(*args, **kwargs):
                if 'time' in kwargs:
                    time = kwargs.get('time')
                    raise TypeError(
                        "The 'time' argument must be passed positionally for 'download()'.\n"
                        f"Instead of `.download(time='{time}')`, use `.download('{time}')`.")
                return attr(*args, **kwargs)
            return wrapper
        
        return attr
    
    @singledispatchmethod
    def fetch_local(self, time):
        """
        Fetch the ERA5 data for a specific time.

        Args:
            time (pd.Timestamp, str, slice): time to fetch from ERA5 weatherbench netCDF files

        Returns:
            ds (xr.Dataset): downloaded dataset
        """
        raise NotImplementedError(
            f"fetch_local method not implemented for type {type(time)}, must be "
            f"<class 'pd.Timestamp'>, <class 'str'>, or <class 'slice'>"
        )

    @fetch_local.register
    @lru_cache(maxsize=10)
    def _(self, time: pd.Timestamp):
        fname = self.download(time)
        return self._read_netcdf(fname)

    @fetch_local.register
    def _(self, time: str):
        time = pd.Timestamp(time)
        return self.fetch_local(time)

    @fetch_local.register
    def _(self, time: slice):
        assert time.step is None, "Step not supported"

        assert isinstance(
            time.start, (pd.Timestamp, str)
        ), "Start must be a pd.Timestamp or str"

        assert isinstance(
            time.stop, (pd.Timestamp, str)
        ), "Stop must be a pd.Timestamp or str"

        dates = pd.date_range(time.start, time.stop)
        if len(dates) > 10:
            self.logger.warning(
                f"\nThe number of requested files is large ({len(dates)}), "
                "consider reducing the range or using .download() instead. \n"
                "If you want to continue, type [Y] to continue, or Enter to end the request..."
            )
            user_input = input(
                f"Fetching {len(dates)} files. Type [Y] to continue,, or Enter end the request..."
            )
            if user_input.lower() != "y":
                return None
        ds_list = [self.fetch_local(t) for t in dates]
        return xr.concat(ds_list, dim="time")

    def _process_before_saving(self, ds):
        return ds.astype("float32")

    def _to_netcdf(self, ds, target_path: str, **kwargs):
        """
        Save the dataset to a fsspec target path.

        Args:
            ds (xr.Dataset): dataset to save
            target_path (str): path to save the dataset to
            **kwargs: passed to the xr.Dataset.to_netcdf function
        """
        # variable encoding to compress the files
        compress = dict(complevel=1, zlib=True, dtype="float32")
        props = dict(encoding={k: compress for k in ds.data_vars}, engine="netcdf4")
        props = props | kwargs

        with tempfile.NamedTemporaryFile() as file:
            # file gets deleted after the context manager exits
            ds.to_netcdf(file.name, **props)
            # make the local directory if it doesn't exist
            target_dir = "/".join(target_path.split("/")[:-1])
            self.fs_local.mkdirs(target_dir, exist_ok=True)
            # upload the file to the target path
            self.fs_local.put(file.name, target_path)

    def _read_netcdf(self, target_path: str):
        """
        Read a netcdf file from the target path

        Args:
            fs (fsspec filesystem): filesystem object
            target_path (str): path to read the file from

        Returns:
            ds (xr.Dataset): dataset read from the file
        """
        with tempfile.NamedTemporaryFile() as file:
            self.fs_local.get(target_path, file.name)
            ds = xr.open_dataset(file.name, engine="netcdf4", chunks={}).load()
        return ds

    def _add_netcdf_attrs(self, ds):
        import subprocess

        res = subprocess.run(["git", "config", "user.email"], stdout=subprocess.PIPE)
        git_username = res.stdout.strip().decode()

        git_info = {}
        if git_username != "":
            git_info["downloader"] = git_username

        ds.attrs = (
            ds.attrs
            | git_info
            | dict(
                processing="downloaded from gs://gcp-public-data-arco-era5/raw/...",
                region_name=self.region_name,
                downloader=git_username,
                requested_bbox=self.bbox,
            )
        )
        return ds

    def __repr__(self):
        text = super().__repr__()[:-2]
        s = self._spacing * " "
        dest_path_formatted = self._make_formatted_dest_path(self.dest_path)
        text += f"\n{s}dest_path = '{dest_path_formatted}',\n)"

        return text

    def __getitem__(self, t):
        return self.download(t)

    def __call__(self, time):
        return self.fetch_local(time)


class ERA5WindFetcher(ERA5Downloader):
    def __init__(
        self,
        bbox_WSEN: tuple = (-180, -90, 180, 90),
        region_name: str = "global",
        dest_path="../data/era5-{region_name}_{resample_time}/{time:%Y}/era5-{region_name}_{resample_time}-winds-{time:%Y%m%d}.nc",
        variables=("10m_u_component_of_wind", "10m_v_component_of_wind"),
        resample_time="1h",
        **kwargs,
    ):
        """
        Fetches ERA5 wind, calculates the first and second moments of wind speed,
        and resamples the data to a different time frequency before saving it
        to a netCDF file.

        Args:
            bbox_WSEN (tuple): bounding box in WSEN format
            region_name (str): name of the region for file naming purposes
            dest_path (str): path to save the netCDF file
            variables (tuple): variables to download
            resample_time (str): time frequency to resample the data to
            kwargs: additional keyword arguments
        """

        self.resample_time = self._prep_resample_time(resample_time)
        kwargs.update(resample_time=self.resample_time)

        super().__init__(
            bbox_WSEN,
            region_name=region_name,
            dest_path=dest_path,
            variables=variables,
            time_steps=range(24),
            **kwargs,
        )

    def _prep_resample_time(self, resample_time):
        dt = pd.Timedelta(resample_time)
        d1 = pd.Timedelta(days=1)

        assert dt <= d1, "Bad resample_time, must be < 1D"
        assert (
            not (d1 / dt) % 1
        ), "Bad resample time, must be a factor of 24 hrs (e.g., 2h, 4h, 1D)"

        # cleaning up the string representation so that 24h is 1D
        resample_time = "1D" if resample_time == "24h" else resample_time

        return resample_time

    def _process_before_saving(self, ds):
        # override the process method to calculate the wind moments
        ds = self._calc_wind_moments(ds)
        ds = self._calc_day_average(ds)
        ds = ds.astype("float32")
        return ds

    def _calc_day_average(self, ds):
        self.logger.debug(f"Resampling time to {self.resample_time}")
        ds = ds.resample(time=self.resample_time).mean(keep_attrs=True)
        return ds

    def _calc_wind_moments(self, ds):
        self.logger.debug("Calculating wind moments")
        ds["wind_moment2"] = ds.u10**2 + ds.v10**2
        ds["wind_moment3"] = abs(ds.u10) ** 3 + abs(ds.v10) ** 3

        description = "Computed on the hourly resolution data with u**m + v**m, where m is the moment"
        ds.wind_moment2.attrs = dict(
            long_name="Second moment of wind speed",
            units="m**2 s**-2",
            description=description,
        )
        ds.wind_moment3.attrs = dict(
            long_name="Third moment of wind speed",
            units="m**3 s**-3",
            description=description,
        )

        return ds

    def __repr__(self):
        cls = super()
        text = cls.__repr__()[:-2]
        s = self._spacing * " "
        text += f"\n{s}resample_time = '{self.resample_time}',\n)"

        return text


def clean_up_cache_dir(
    path="./era5_downloader_tmp/",
    remove_older_n_than_days: float = 1,
    force_remove_all=False,
):
    """
    Cleans up the cache directory by removing empty folders and folders older than a given age.

    Args:
        path (str): path to the cache directory
        remove_older_n_than_days (float): remove folders older than this many days
        force_remove_all (bool): remove all folders regardless of age or contents

    Returns:
        None
    """

    def folder_age_days(fname):
        try:
            created = pd.to_datetime(fname.split("_")[0], format="%Y%m%d%H%M%S")
            age = pd.Timestamp.now() - created
        except ValueError:
            age = pd.Timedelta(days=999)

        return age.total_seconds() / 86400

    logr = logger.bind(custom="CleanUp")
    path = pathlib.Path(path)
    paths = [f for f in path.iterdir() if f.is_dir()]
    ages = [folder_age_days(f.name) for f in paths]

    remaining_size = 0
    cleaned_size = 0
    counts = 0
    for subdir, subdir_age in zip(paths, ages):
        flist = list(subdir.iterdir())

        is_old = subdir_age > remove_older_n_than_days
        is_empty = len(flist) == 0
        is_forced = force_remove_all

        # folder must be old and empty to be removed or, overridden by being forced
        clean_folder = is_forced or (is_old and is_empty)

        if clean_folder:
            folder_contents_size = (
                sum(f.stat().st_size for f in subdir.iterdir()) / 1024**2
            )
            cleaned_size += folder_contents_size

            [f.unlink() for f in subdir.iterdir()]
            subdir.rmdir()
            logr.info(
                f"Removed folder and contents ({folder_contents_size:.2f} MB): {subdir}"
            )
            logr.debug(f"Folder {subdir} was {subdir_age:.3f} days old")
            counts += 1
            continue  # skip the remaining size calculation

        elif not is_empty:
            logr.info(f"Folder {subdir} is not empty")

        elif not is_old:
            logr.info(
                f"Folder {subdir} is not old enough ({subdir_age:.2f} days < {remove_older_n_than_days} days)"
            )

        remaining_size += sum(f.stat().st_size for f in subdir.iterdir()) / 1024**2

    if counts >= 1:
        logr.success(
            f"Removed {counts} folders {cleaned_size:.2f} MB; Remaining cache: {remaining_size:.2f} MB"
        )
    else:
        logr.info(f"No folders removed; Remaining cache: {remaining_size:.2f} MB")
