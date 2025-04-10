from .core import ERA5Downloader

CRYOGRID_DEFAULT_LEVELS = (300, 500, 600, 700, 800, 850, 900, 1000)
CRYOGRID_DEFAULT_VARIABLES = (
    "geopotential",  # will fetch both surface and pressure_levels
    "temperature",
    "specific_humidity",
    "u_component_of_wind",
    "v_component_of_wind",
    "2m_dewpoint_temperature",
    "surface_thermal_radiation_downwards",
    "surface_solar_radiation_downwards",
    "toa_incident_solar_radiation",
    "10m_u_component_of_wind",
    "10m_v_component_of_wind",
    "surface_pressure",
    "total_precipitation",
    "2m_temperature",
)


def create_cryogrid_forcing_fetcher(
    bbox_WSEN: tuple,
    region_name: str,
    dest_path="../data/era5-{region_name}/{time:%Y}/era5-cryogrid_forcing-{region_name}-{time:%Y%m%d}.nc",
    levels=CRYOGRID_DEFAULT_LEVELS,
    variables=CRYOGRID_DEFAULT_VARIABLES,
    **kwargs,
):
    return ERA5Downloader(
        bbox_WSEN=bbox_WSEN,
        region_name=region_name,
        dest_path=dest_path,
        levels=levels,
        variables=variables,
        **kwargs,
    )
