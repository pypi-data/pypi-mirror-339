# ERA5-Downloader

A lightweight and efficient tool for downloading ERA5 climate data, optimized for time series retrieval.

This package leverages `fsspec` and `xarray` to handle remote datasets, providing an alternative to the Copernicus Climate Data Store (CDS) for accessing ERA5 data. It is designed to optimize workflows by focusing on downloading and processing only the necessary data for your region and time period.

## Installation

Install the package using `pip`:

```sh
pip install era5-downloader
```

## Data Sources

- **ERA5 data:** The ERA5 data is created by ECMWF. The ERA5 dataset is a global atmospheric reanalysis that covers the period from 1940 to present at hourly intervals and a spatial resolution of 0.25 degrees. The ERA5 data is made available through the Copernicus Climate Data Store (CDS). However the CDS API can be very slow, especially for large requests. 
[Learn more about ERA5](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels?tab=overview)

- **Google Cloud Public Datasets:** Google has a copy of the ERA5 data available on [Google Public Datasets](https://cloud.google.com/storage/docs/public-datasets/era5). This data is free to access and download. There are three formats: [raw (raw), cloud optimized (co), and analysis ready (ar)](https://cloud.google.com/storage/docs/public-datasets/era5). For time series data that doesn't use all the levels, I've found that downloading the raw netCDF files is actually faster than using the `zarr` store. This can be done in parallel and you are only limited by your connection speed. 


## Usage

```python
import era5_downloader as era5down

local_path = "../data/era5-{region_name}/{time:%Y}/era5-{region_name}-{time:%Y%m%d}.nc"
era5data = era5down.ERA5Downloader(
    bbox_WSEN=(-10, 35, 10, 45),  # Bounding box: West, South, East, North
    region_name="example_region",  # variable passed here will be substituted in the local path (for better naming practices)
    dest_path=local_path,  # can also be an S3 bucket with format "s3://bucket-name/era5-{region_name}/...
    levels=[500, 700, 850],  # Pressure levels (can also be None)
    variables=["temperature", "specific_humidity"]
)

# Download data for a specific day
file_name = era5data.download(time="2023-01-01")  
file_name = era5data["2023-01-01"]  # the same as above

# Download data for a range of days
file_list = era5data.download(time=slice("2023-01-01", "2023-01-10"))  # Fetch a range of days
file_list = era5data["2023-01-01" : "2023-01-10"]  # the same as above

# get local file if it exists, otherwise download it, and then return as xarray dataset
ds = era5data.fetch_local("2023-01-01")  
ds = era5data.fetch_local(time=slice("2023-01-01", "2023-01-10"))  # Fetch a range of days 

```

There is a function to launc a downloader for [CryoGrid](https://gmd.copernicus.org/articles/16/2607/2023/) forcing data:
```python
cryogrid_forcing = era5down.launch_cryogrid_downloader(
    bbox_WSEN=(-10, 35, 10, 45),  # Bounding box: West, South, East, North
    region_name="example_region",
    dest_path="../data/era5-{region_name}/{time:%Y}/era5-{region_name}-{time:%Y%m%d}.nc",)

cryogrid_forcing["2023-01-01"]
```

## How It Works

1. Initiate the downloader class with the bounding box (`bbox_WSEN`) and the variables you'd like - e.g., temperature, precipitation, etc. The pressure_level or single_level can be grouped together - the downloader will automatically fetch the appropriate data.
2. Specify a time for the data you want to download. 
3. raw netCDF files are cached to your local machine in a temporary directory.
4. Data are extracted for the specified geographical region defined by a bounding box (`bbox_WSEN`)
5. The requested subset of data  is saved to the specified local path in NetCDF format

## Available Levels and Variables
```python
pressure_levels = [
    1, 2, 3, 5, 7, 10, 20, 30, 50, 70,
    100, 125, 150, 175, 200, 225, 250,
    300, 350, 400, 450, 500, 550, 600,
    650, 700, 750, 775, 800, 825, 850,
    875, 900, 925, 950, 975, 1000]

pressure_level_variables = [
    'fraction_of_cloud_cover',
    'geopotential',
    'ozone_mass_mixing_ratio',
    'potential_vorticity',
    'specific_cloud_ice_water_content',
    'specific_cloud_liquid_water_content',
    'specific_humidity',
    'temperature',
    'u_component_of_wind',
    'v_component_of_wind',
    'vertical_velocity']

single_level_variables = [
    '100m_u_component_of_wind',
    '100m_v_component_of_wind',
    '10m_u_component_of_neutral_wind',
    '10m_u_component_of_wind',
    '10m_v_component_of_neutral_wind',
    '10m_v_component_of_wind',
    '10m_wind_gust_since_previous_post_processing',
    '2m_dewpoint_temperature',
    '2m_temperature',
    'air_density_over_the_oceans',
    'angle_of_sub_gridscale_orography',
    'anisotropy_of_sub_gridscale_orography',
    'benjamin_feir_index',
    'boundary_layer_dissipation',
    'boundary_layer_height',
    'charnock',
    'clear_sky_direct_solar_radiation_at_surface',
    'cloud_base_height',
    'coefficient_of_drag_with_waves',
    'convective_available_potential_energy',
    'convective_inhibition',
    'convective_precipitation',
    'convective_rain_rate',
    'convective_snowfall',
    'convective_snowfall_rate_water_equivalent',
    'downward_uv_radiation_at_the_surface',
    'duct_base_height',
    'eastward_gravity_wave_surface_stress',
    'eastward_turbulent_surface_stress',
    'evaporation',
    'forecast_albedo',
    'forecast_logarithm_of_surface_roughness_for_heat',
    'forecast_surface_roughness',
    'free_convective_velocity_over_the_oceans',
    'friction_velocity',
    'geopotential',
    'gravity_wave_dissipation',
    'high_cloud_cover',
    'high_vegetation_cover',
    'ice_temperature_layer_1',
    'ice_temperature_layer_2',
    'ice_temperature_layer_3',
    'ice_temperature_layer_4',
    'instantaneous_10m_wind_gust',
    'instantaneous_eastward_turbulent_surface_stress',
    'instantaneous_large_scale_surface_precipitation_fraction',
    'instantaneous_moisture_flux',
    'instantaneous_northward_turbulent_surface_stress',
    'instantaneous_surface_sensible_heat_flux',
    'k_index',
    'lake_bottom_temperature',
    'lake_cover',
    'lake_depth',
    'lake_ice_depth',
    'lake_ice_temperature',
    'lake_mix_layer_depth',
    'lake_mix_layer_temperature',
    'lake_shape_factor',
    'lake_total_layer_temperature',
    'land_sea_mask',
    'large_scale_precipitation',
    'large_scale_precipitation_fraction',
    'large_scale_rain_rate',
    'large_scale_snowfall',
    'large_scale_snowfall_rate_water_equivalent',
    'leaf_area_index_high_vegetation',
    'leaf_area_index_low_vegetation',
    'low_cloud_cover',
    'low_vegetation_cover',
    'maximum_2m_temperature_since_previous_post_processing',
    'maximum_individual_wave_height',
    'maximum_total_precipitation_rate_since_previous_post_processing',
    'mean_boundary_layer_dissipation',
    'mean_convective_precipitation_rate',
    'mean_convective_snowfall_rate',
    'mean_direction_of_total_swell',
    'mean_direction_of_wind_waves',
    'mean_eastward_gravity_wave_surface_stress',
    'mean_eastward_turbulent_surface_stress',
    'mean_evaporation_rate',
    'mean_gravity_wave_dissipation',
    'mean_large_scale_precipitation_fraction',
    'mean_large_scale_precipitation_rate',
    'mean_large_scale_snowfall_rate',
    'mean_northward_gravity_wave_surface_stress',
    'mean_northward_turbulent_surface_stress',
    'mean_period_of_total_swell',
    'mean_period_of_wind_waves',
    'mean_potential_evaporation_rate',
    'mean_runoff_rate',
    'mean_sea_level_pressure',
    'mean_snow_evaporation_rate',
    'mean_snowfall_rate',
    'mean_snowmelt_rate',
    'mean_square_slope_of_waves',
    'mean_sub_surface_runoff_rate',
    'mean_surface_direct_short_wave_radiation_flux',
    'mean_surface_direct_short_wave_radiation_flux_clear_sky',
    'mean_surface_downward_long_wave_radiation_flux',
    'mean_surface_downward_long_wave_radiation_flux_clear_sky',
    'mean_surface_downward_short_wave_radiation_flux',
    'mean_surface_downward_short_wave_radiation_flux_clear_sky',
    'mean_surface_downward_uv_radiation_flux',
    'mean_surface_latent_heat_flux',
    'mean_surface_net_long_wave_radiation_flux',
    'mean_surface_net_long_wave_radiation_flux_clear_sky',
    'mean_surface_net_short_wave_radiation_flux',
    'mean_surface_net_short_wave_radiation_flux_clear_sky',
    'mean_surface_runoff_rate',
    'mean_surface_sensible_heat_flux',
    'mean_top_downward_short_wave_radiation_flux',
    'mean_top_net_long_wave_radiation_flux',
    'mean_top_net_long_wave_radiation_flux_clear_sky',
    'mean_top_net_short_wave_radiation_flux',
    'mean_top_net_short_wave_radiation_flux_clear_sky',
    'mean_total_precipitation_rate',
    'mean_vertical_gradient_of_refractivity_inside_trapping_layer',
    'mean_vertically_integrated_moisture_divergence',
    'mean_wave_direction',
    'mean_wave_direction_of_first_swell_partition',
    'mean_wave_direction_of_second_swell_partition',
    'mean_wave_direction_of_third_swell_partition',
    'mean_wave_period',
    'mean_wave_period_based_on_first_moment',
    'mean_wave_period_based_on_first_moment_for_swell',
    'mean_wave_period_based_on_first_moment_for_wind_waves',
    'mean_wave_period_based_on_second_moment_for_swell',
    'mean_wave_period_based_on_second_moment_for_wind_waves',
    'mean_wave_period_of_first_swell_partition',
    'mean_wave_period_of_second_swell_partition',
    'mean_wave_period_of_third_swell_partition',
    'mean_zero_crossing_wave_period',
    'medium_cloud_cover',
    'minimum_2m_temperature_since_previous_post_processing',
    'minimum_total_precipitation_rate_since_previous_post_processing',
    'minimum_vertical_gradient_of_refractivity_inside_trapping_layer',
    'model_bathymetry',
    'near_ir_albedo_for_diffuse_radiation',
    'near_ir_albedo_for_direct_radiation',
    'normalized_energy_flux_into_ocean',
    'normalized_energy_flux_into_waves',
    'normalized_stress_into_ocean',
    'northward_gravity_wave_surface_stress',
    'northward_turbulent_surface_stress',
    'ocean_surface_stress_equivalent_10m_neutral_wind_direction',
    'ocean_surface_stress_equivalent_10m_neutral_wind_speed',
    'peak_wave_period',
    'period_corresponding_to_maximum_individual_wave_height',
    'potential_evaporation',
    'precipitation_type',
    'runoff',
    'sea_ice_cover',
    'sea_surface_temperature',
    'significant_height_of_combined_wind_waves_and_swell',
    'significant_height_of_total_swell',
    'significant_height_of_wind_waves',
    'significant_wave_height_of_first_swell_partition',
    'significant_wave_height_of_second_swell_partition',
    'significant_wave_height_of_third_swell_partition',
    'skin_reservoir_content',
    'skin_temperature',
    'slope_of_sub_gridscale_orography',
    'snow_albedo',
    'snow_density',
    'snow_depth',
    'snow_evaporation',
    'snowfall',
    'snowmelt',
    'soil_temperature_level_1',
    'soil_temperature_level_2',
    'soil_temperature_level_3',
    'soil_temperature_level_4',
    'soil_type',
    'standard_deviation_of_filtered_subgrid_orography',
    'standard_deviation_of_orography',
    'sub_surface_runoff',
    'surface_latent_heat_flux',
    'surface_net_solar_radiation',
    'surface_net_solar_radiation_clear_sky',
    'surface_net_thermal_radiation',
    'surface_net_thermal_radiation_clear_sky',
    'surface_pressure',
    'surface_runoff',
    'surface_sensible_heat_flux',
    'surface_solar_radiation_downward_clear_sky',
    'surface_solar_radiation_downwards',
    'surface_thermal_radiation_downward_clear_sky',
    'surface_thermal_radiation_downwards',
    'temperature_of_snow_layer',
    'toa_incident_solar_radiation',
    'top_net_solar_radiation',
    'top_net_solar_radiation_clear_sky',
    'top_net_thermal_radiation',
    'top_net_thermal_radiation_clear_sky',
    'total_cloud_cover',
    'total_column_cloud_ice_water',
    'total_column_cloud_liquid_water',
    'total_column_ozone',
    'total_column_rain_water',
    'total_column_snow_water',
    'total_column_supercooled_liquid_water',
    'total_column_water',
    'total_column_water_vapour',
    'total_precipitation',
    'total_sky_direct_solar_radiation_at_surface',
    'total_totals_index',
    'trapping_layer_base_height',
    'trapping_layer_top_height',
    'type_of_high_vegetation',
    'type_of_low_vegetation',
    'u_component_stokes_drift',
    'uv_visible_albedo_for_diffuse_radiation',
    'uv_visible_albedo_for_direct_radiation',
    'v_component_stokes_drift',
    'vertical_integral_of_divergence_of_cloud_frozen_water_flux',
    'vertical_integral_of_divergence_of_cloud_liquid_water_flux',
    'vertical_integral_of_divergence_of_geopotential_flux',
    'vertical_integral_of_divergence_of_kinetic_energy_flux',
    'vertical_integral_of_divergence_of_mass_flux',
    'vertical_integral_of_divergence_of_moisture_flux',
    'vertical_integral_of_divergence_of_ozone_flux',
    'vertical_integral_of_divergence_of_thermal_energy_flux',
    'vertical_integral_of_divergence_of_total_energy_flux',
    'vertical_integral_of_eastward_cloud_frozen_water_flux',
    'vertical_integral_of_eastward_cloud_liquid_water_flux',
    'vertical_integral_of_eastward_geopotential_flux',
    'vertical_integral_of_eastward_heat_flux',
    'vertical_integral_of_eastward_kinetic_energy_flux',
    'vertical_integral_of_eastward_mass_flux',
    'vertical_integral_of_eastward_ozone_flux',
    'vertical_integral_of_eastward_total_energy_flux',
    'vertical_integral_of_eastward_water_vapour_flux',
    'vertical_integral_of_energy_conversion',
    'vertical_integral_of_kinetic_energy',
    'vertical_integral_of_mass_of_atmosphere',
    'vertical_integral_of_mass_tendency',
    'vertical_integral_of_northward_cloud_frozen_water_flux',
    'vertical_integral_of_northward_cloud_liquid_water_flux',
    'vertical_integral_of_northward_geopotential_flux',
    'vertical_integral_of_northward_heat_flux',
    'vertical_integral_of_northward_kinetic_energy_flux',
    'vertical_integral_of_northward_mass_flux',
    'vertical_integral_of_northward_ozone_flux',
    'vertical_integral_of_northward_total_energy_flux',
    'vertical_integral_of_northward_water_vapour_flux',
    'vertical_integral_of_potential_and_internal_energy',
    'vertical_integral_of_potential_internal_and_latent_energy',
    'vertical_integral_of_temperature',
    'vertical_integral_of_thermal_energy',
    'vertical_integral_of_total_energy',
    'vertically_integrated_moisture_divergence',
    'volumetric_soil_water_layer_1',
    'volumetric_soil_water_layer_2',
    'volumetric_soil_water_layer_3',
    'volumetric_soil_water_layer_4',
    'wave_spectral_directional_width',
    'wave_spectral_directional_width_for_swell',
    'wave_spectral_directional_width_for_wind_waves',
    'wave_spectral_kurtosis',
    'wave_spectral_peakedness',
    'wave_spectral_skewness',
    'zero_degree_level']

```


## Contributing

Contributions are welcome! If you encounter issues, please open an issue or submit a pull request on GitHub.

## License

This project is licensed under the MIT License.