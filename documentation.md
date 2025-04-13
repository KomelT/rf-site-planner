# Documentation

## Splat
### class Splat
SPLAT! wrapper class. Provides methods for generating SPLAT! RF coverage maps in GeoTIFF format.
This class automatically downloads and caches the necessary terrain data from AWS:
https://registry.opendata.aws/terrain-tiles/.

SPLAT! and its optional utilities (splat, splat-hd, srtm2sdf, srtm2sdf-hd) must be installed
in the `splat_path` directory and be executable.

See the SPLAT! documentation: https://www.qsl.net/kd2bd/splat.html
Additional details: https://github.com/jmcmellen/splat

Args:
    splat_path (str): Path to the directory containing the SPLAT! binaries.
    cache_dir (str): Directory to store cached terrain tiles.
    cache_size_gb (float): Maximum size of the cache in gigabytes (GB). Defaults to 1.0.
        When the size of the cached tiles exceeds this value, the oldest tiles are deleted
        and will be re-downloaded as required.
    bucket_name (str): Name of the S3 bucket containing terrain tiles. Defaults to the AWS
        open data bucket `elevation-tiles-prod`.
    bucket_prefix (str): Folder in the S3 bucket containing the terrain tiles. Defaults to
        `v2/skadi`, which contains 1-arcsecond terrain data for most of the world.

### def coverage_prediction
Execute a SPLAT! coverage prediction using the provided CoveragePredictionRequest.

Args:
    request (CoveragePredictionRequest): The coverage prediction request object.

Returns:
    bytes: the SPLAT! coverage prediction as a GeoTIFF.

Raises:
    RuntimeError: If SPLAT! fails to execute.

### def _calculate_required_terrain_tiles
Determine the set of required terrain tiles for the specified area and their corresponding .sdf / -hd.sdf
filenames. This is used for downloading terrain data for SPLAT! which requires the files to follow a specific
naming convention.

Calculates the geographic bounding box based on the provided latitude, longitude, and radius, then
determines the necessary tiles to cover the area. It returns filenames in the following formats:

    - .hgt.gz files: raw 1 arc-second terrain elevation tiles stored in AWS Open Data / S3.
    - .sdf files: Used for standard resolution (3-arcsecond) terrain data in SPLAT!.
    - .sdf-hd files: Used for high-resolution (1-arcsecond) terrain data in SPLAT!.

The .hgt.gz filenames have the format:
    <N|S><latitude: 2 digits><E|W><longitude: 3 digits>.hgt.gz
    Example: N35W120.hgt.gz

The .sdf and .sdf-hd filenames have the format:
    <lat_start>:<lat_end>:<lon_start>:<lon_end>.sdf
    <lat_start>:<lat_end>:<lon_start>:<lon_end>-hd.sdf
    Example: 35:36:-120:-119.sdf, 35:36:-120:-119-hd.sdf

Args:
    lat (float): Latitude of the center point in degrees.
    lon (float): Longitude of the center point in degrees.
    radius (float): Simulation coverage radius in meters.

Returns:
    List[Tuple[str, str, str]]: A list of tuples, each containing:
        - .hgt.gz filename (str)
        - Corresponding .sdf filename (str)
        - Corresponding .sdf-hd filename (str)

### def _create_splat_qth
Generate the contents of a SPLAT! .qth file describing a transmitter or receiver site.

Args:
    name (str): Name of the site (unused but required for SPLAT!).
    latitude (float): Latitude of the site in degrees.
    longitude (float): Longitude of the site in degrees.
    elevation (float): Elevation (AGL) of the site in meters.

Returns:
    bytes: The content of the .qth file formatted for SPLAT!.

### def _create_splat_lrp
Generate the contents of a SPLAT! .lrp file describing environment and propagation parameters.

Args:
    ground_dielectric (float): Earth's dielectric constant.
    ground_conductivity (float): Earth's conductivity (Siemens per meter).
    atmosphere_bending (float): Atmospheric bending constant.
    frequency_mhz (float): Frequency in MHz.
    radio_climate (str): Radio climate type.
    polarization (str): Antenna polarization.
    situation_fraction (float): Fraction of situations (percentage, 0-100).
    time_fraction (float): Fraction of time (percentage, 0-100).
    tx_power (float): Transmitter power in dBm.
    tx_gain (float): Transmitter antenna gain in dB.
    system_loss (float): System losses in dB (e.g., cable loss).

Returns:
    bytes: The content of the .lrp file formatted for SPLAT!.

### def _create_splat_dcf
Generate the content of a SPLAT! .dcf file controlling the signal level contours
using the specified Matplotlib color map.

Args:
    colormap_name (str): The name of the Matplotlib colormap.
    min_dbm (float): The minimum signal strength value for the colormap in dBm.
    max_dbm (float): The maximum signal strength value for the colormap in dBm.

Returns:
    bytes: The content of the .dcf file formatted for SPLAT!.

### def create_splat_colorbar
Generate a list of RGB color values corresponding to the color map, min and max RSSI values in dBm.

### def _create_splat_geotiff
Generate GeoTIFF file content from SPLAT! PPM and KML data, with transparency for null areas.

Args:
    ppm_bytes (bytes): Binary content of the SPLAT-generated PPM file.
    kml_bytes (bytes): Binary content of the KML file containing geospatial bounds.
    colormap_name (str): Name of the matplotlib colormap to use for the GeoTIFF.
    min_dbm (float): Minimum dBm value for the colormap scale.
    max_dbm (float): Maximum dBm value for the colormap scale.
    null_value (int): Pixel value in the PPM that represents null areas. Defaults to 255.

Returns:
    bytes: The binary content of the resulting GeoTIFF file.

Raises:
    RuntimeError: If the conversion process fails.

### def _download_terrain_tile
Downloads a terrain tile from the S3 bucket if not found in the local cache.

This method checks if the requested tile is available in the cache..
If the tile is not cached, it downloads the tile from the specified S3 bucket,
stores it in the cache, and returns the tile data.

Args:
    tile_name (str): The name of the terrain tile to be downloaded.

Returns:
    bytes: The binary content of the terrain tile.

Raises:
    Exception: If the tile cannot be downloaded from S3.


### def _hgt_filename_to_sdf_filename
helper method to get the expected SPLAT! .sdf filename from the .hgt.gz terrain tile.

### def _convert_hgt_to_sdf
Converts a .hgt.gz terrain tile (provided as bytes) to a SPLAT! .sdf or -hd.sdf file.

This method checks if the converted .sdf or -hd.sdf file corresponding to the tile_name
exists in the cache. If not, the method decompresses the tile, places it in a temporary
directory, performs the conversion using the SPLAT! utility (srtm2sdf or srtm2sdf-hd),
and caches the resulting .sdf file.

Args:
    tile (bytes): The binary content of the .hgt.gz terrain tile.
    tile_name (str): The name of the terrain tile (e.g., N35W120.hgt.gz).
    high_resolution (bool): Whether to generate a high-resolution -hd.sdf file. Defaults to False.

Returns:
    bytes: The binary content of the converted .sdf or -hd.sdf file.

Raises:
    RuntimeError: If the conversion fails.