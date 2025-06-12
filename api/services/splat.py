import gzip
import io
import logging
import math
import os
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from json import dumps
from typing import List, Literal, Tuple

import boto3
import matplotlib.pyplot as plt
import numpy as np
import rasterio
from botocore import UNSIGNED
from botocore.config import Config
from botocore.exceptions import ClientError
from diskcache import Cache
from models.CoveragePredictionRequest import CoveragePredictionRequest
from models.LosPredictionRequest import LosPredictionRequest
from PIL import Image
from rasterio.enums import Resampling
from rasterio.transform import Affine, from_bounds

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logging.getLogger("boto3").setLevel(logging.WARNING)
logging.getLogger("botocore").setLevel(logging.WARNING)
logging.getLogger("s3transfer").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


class Splat:
    def __init__(
        self,
        splat_path: str,
        cache_dir: str = ".splat_tiles",
        cache_size_gb: float = 1.0,
        bucket_name: str = "elevation-tiles-prod",
        bucket_prefix: str = "v2/skadi",
    ):
        # Check the provided SPLAT! path exists
        if not os.path.isdir(splat_path):
            raise FileNotFoundError(
                f"Provided SPLAT! path '{splat_path}' is not a valid directory."
            )

        # SPLAT! binaries
        self.splat_binary = os.path.join(splat_path, "splat")  # core SPLAT! program
        self.splat_hd_binary = os.path.join(
            splat_path, "splat-hd"
        )  # used instead of the splat binary when using the 1-arcsecond / 30 meter resolution terrain data.
        self.srtm2sdf_binary = os.path.join(
            splat_path, "srtm2sdf"
        )  # convert 3-arcsecond resolution srtm .hgt terrain tiles to SPLAT! .sdf terrain tiles.
        self.srtm2sdf_hd_binary = os.path.join(
            splat_path, "srtm2sdf-hd"
        )  # used instead of srtm2sdf when using the 1-arcsecond / 30 meter resolution terrain data.

        # Check the SPLAT! binaries exist and are executable
        if not os.path.isfile(self.splat_binary) or not os.access(
            self.splat_binary, os.X_OK
        ):
            raise FileNotFoundError(
                f"'splat' binary not found or not executable at '{self.splat_binary}'"
            )
        if not os.path.isfile(self.splat_hd_binary) or not os.access(
            self.splat_hd_binary, os.X_OK
        ):
            raise FileNotFoundError(
                f"'splat-hd' binary not found or not executable at '{self.splat_hd_binary}'"
            )
        if not os.path.isfile(self.srtm2sdf_binary) or not os.access(
            self.srtm2sdf_binary, os.X_OK
        ):
            raise FileNotFoundError(
                f"'srtm2sdf_binary' binary not found or not executable at '{self.srtm2sdf_binary}'"
            )
        if not os.path.isfile(self.srtm2sdf_hd_binary) or not os.access(
            self.srtm2sdf_hd_binary, os.X_OK
        ):
            raise FileNotFoundError(
                f"'srtm2sdf_hd_binary' binary not found or not executable at '{self.srtm2sdf_hd_binary}'"
            )

        self.tile_cache = Cache(
            cache_dir, size_limit=int(cache_size_gb * 1024 * 1024 * 1024)
        )

        self.s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))
        self.bucket_name = bucket_name
        self.bucket_prefix = bucket_prefix

        logger.info(
            f"Initialized SPLAT! with terrain tile cache at '{cache_dir}' with a size limit of {cache_size_gb} GB."
        )

    def los_prediction(self, request: LosPredictionRequest) -> bytes:
        logger.debug(f"LOS prediction request: {request.json()}")

        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                logger.debug(f"Temporary directory created: {tmpdir}")

                # FIXME: Eventually support high-resolution terrain data
                request.high_resolution = False

                # determine the required terrain tiles
                required_tiles = Splat._calculate_required_terrain_tiles_los(
                    request.tx_lat,
                    request.tx_lon,
                    request.rx_lat,
                    request.rx_lon,
                )

                self._download_convert_tiles(
                    self, required_tiles, request.high_resolution, tmpdir
                )

                # write transmitter qth file
                with open(os.path.join(tmpdir, "tx.qth"), "wb") as qth_file:
                    qth_file.write(
                        Splat._create_splat_qth(
                            "tx",
                            request.tx_lat,
                            request.tx_lon,
                            request.tx_height * (100 / 30.48),
                        )
                    )

                # write reciver qth file
                with open(os.path.join(tmpdir, "rx.qth"), "wb") as qth_file:
                    qth_file.write(
                        Splat._create_splat_qth(
                            "rx",
                            request.rx_lat,
                            request.rx_lon,
                            request.rx_height * (100 / 30.48),
                        )
                    )

                # write model parameter / lrp file
                with open(os.path.join(tmpdir, "splat.lrp"), "wb") as lrp_file:
                    logger.debug(request.tx_power)
                    lrp_file.write(
                        Splat._create_splat_lrp(
                            ground_dielectric=request.ground_dielectric,
                            ground_conductivity=request.ground_conductivity,
                            atmosphere_bending=request.atmosphere_bending,
                            frequency_mhz=request.frequency_mhz,
                            radio_climate=request.radio_climate,
                            polarization=request.polarization,
                            situation_fraction=request.situation_fraction,
                            time_fraction=request.time_fraction,
                            tx_power=request.tx_power,
                            tx_gain=request.tx_gain + request.rx_gain,
                            system_loss=request.system_loss,
                        )
                    )

                logger.debug(f"Contents of {tmpdir}: {os.listdir(tmpdir)}")

                splat_command = [
                    (
                        self.splat_hd_binary
                        if request.high_resolution
                        else self.splat_binary
                    ),
                    "-t",
                    "tx.qth",
                    "-r",
                    "rx.qth",
                    # "-c",
                    # str(request.rx_height),
                    "-gc",
                    str(request.clutter_height),
                    "-db",
                    str(request.signal_threshold),
                    "-gpsav",
                    "-f",
                    "868.5M",
                    "-H",
                    "normalized_terrain_height_graph.png",
                    "-l",
                    "path_loss_graph.png",
                    "-olditm",
                    "-metric",
                ]  # flag "olditm" uses the standard ITM model instead of ITWOM, which has produced unrealistic results.
                logger.debug(f"Executing SPLAT! command: {' '.join(splat_command)}")

                splat_result = subprocess.run(
                    splat_command,
                    cwd=tmpdir,
                    capture_output=True,
                    text=True,
                    check=False,
                )

                logger.debug(f"Contents of {tmpdir}: {os.listdir(tmpdir)}")

                logger.debug(f"SPLAT! stdout:\n{splat_result.stdout}")
                logger.debug(f"SPLAT! stderr:\n{splat_result.stderr}")

                if splat_result.returncode != 0:
                    logger.error(
                        f"SPLAT! execution failed with return code {splat_result.returncode}"
                    )
                    raise RuntimeError(
                        f"SPLAT! execution failed with return code {splat_result.returncode}\n"
                        f"Stdout: {splat_result.stdout}\nStderr: {splat_result.stderr}"
                    )

                logger.info("SPLAT! coverage prediction completed successfully.")

                # save all files from tmpdir to /var/app/geoserver_data
                """
                for filename in os.listdir(tmpdir):
                    if filename.endswith(".kml") or filename.endswith(".ppm"):
                        continue
                    src_path = os.path.join(tmpdir, filename)
                    dst_path = os.path.join("/var/app/geoserver_data/tmp", filename)
                    with open(src_path, "rb") as src_file:
                        with open(dst_path, "wb") as dst_file:
                            dst_file.write(src_file.read())
                """

                with open(os.path.join(tmpdir, "profile.gp"), "rb") as profile_file:
                    with open(
                        os.path.join(tmpdir, "curvature.gp"), "rb"
                    ) as curvature_file:
                        with open(
                            os.path.join(tmpdir, "fresnel.gp"), "rb"
                        ) as fresnel_file:
                            with open(
                                os.path.join(tmpdir, "reference.gp"), "rb"
                            ) as reference_file:
                                with open(
                                    os.path.join(tmpdir, "tx-to-rx.txt"), "rb"
                                ) as tx_to_rx_file:
                                    profile_data = profile_file.read()
                                    curvature_data = curvature_file.read()
                                    fresnel_data = fresnel_file.read()
                                    reference_data = reference_file.read()
                                    tx_to_rx_data = tx_to_rx_file.read()

                                    profile_lines = profile_data.decode(
                                        "utf-8"
                                    ).splitlines()
                                    curvature_lines = curvature_data.decode(
                                        "utf-8"
                                    ).splitlines()
                                    fresnel_lines = fresnel_data.decode(
                                        "utf-8"
                                    ).splitlines()
                                    reference_lines = reference_data.decode(
                                        "utf-8"
                                    ).splitlines()

                                    distance = []
                                    profile = []
                                    curvature = []
                                    fresnel = []
                                    reference = []

                                    for line in profile_lines:
                                        try:
                                            d, p = line.split("\t")
                                            distance.append(float(d))
                                            profile.append(float(p))
                                        except ValueError:
                                            logger.warning(
                                                f"Skipping invalid line in profile: {line}"
                                            )

                                    for line in curvature_lines:
                                        try:
                                            d, c = line.split("\t")
                                            curvature.append(float(c))
                                        except ValueError:
                                            logger.warning(
                                                f"Skipping invalid line in curvature: {line}"
                                            )

                                    for line in fresnel_lines:
                                        try:
                                            d, f = line.split("\t")
                                            fresnel.append(float(f))
                                        except ValueError:
                                            logger.warning(
                                                f"Skipping invalid line in fresnel: {line}"
                                            )

                                    for line in reference_lines:
                                        try:
                                            d, r = line.split("\t")
                                            reference.append(float(r))
                                        except ValueError:
                                            logger.warning(
                                                f"Skipping invalid line in reference: {line}"
                                            )

                                    tx_to_rx_lines = tx_to_rx_data.splitlines()
                                    path_obstruction = True
                                    path_message = ""
                                    path_obstructions = []

                                    first_freshnel_obstruction = True
                                    first_freshnel_message = ""

                                    for i, line in enumerate(tx_to_rx_lines):
                                        if (
                                            b"No obstructions to LOS path due to terrain were detected by SPLAT!"
                                            in line
                                        ):
                                            path_obstruction = False
                                        elif (
                                            b"The first Fresnel zone is clear." in line
                                        ):
                                            first_freshnel_obstruction = False

                                        elif (
                                            b"Between rx and tx, SPLAT! detected obstructions at:"
                                            in line
                                        ):
                                            for line in tx_to_rx_lines[i + 2 :]:
                                                if line.strip() == b"":
                                                    break

                                                decoded_parts = [
                                                    part.decode("utf-8").strip()
                                                    for part in line.strip().split(
                                                        b", "
                                                    )
                                                ]

                                                decoded_parts = [
                                                    float(part.split(" ")[0])
                                                    for part in decoded_parts
                                                ]

                                                val = decoded_parts[1]
                                                original_longitude = (
                                                    360 - val if val > 180 else -val
                                                )
                                                decoded_parts[1] = original_longitude

                                                path_obstructions.append(decoded_parts)

                                        elif (
                                            b"to clear all obstructions detected by SPLAT!."
                                            in line
                                        ):
                                            path_message = f"{tx_to_rx_lines[i + 1].strip()} {line.strip()}"

                                        elif (
                                            b"to clear the first Fresnel zone." in line
                                        ):
                                            first_freshnel_message = f"{tx_to_rx_lines[i + 1].strip()} {line.strip()}"

                                    # extract number from "Signal power level at rx: -110.14 dBm"
                                    signal_power_line = ""
                                    for line in tx_to_rx_lines:
                                        if b"Signal power level at rx:" in line:
                                            signal_power_line = (
                                                line.strip()
                                                .split(b" ")[5]
                                                .strip()
                                                .decode("utf-8")
                                            )
                                            break

                                    return dumps(
                                        {
                                            "distance": distance,
                                            "profile": profile,
                                            "curvature": curvature,
                                            "fresnel": fresnel,
                                            "reference": reference,
                                            "path": {
                                                "obstructed": path_obstruction,
                                                "message": path_message,
                                                "obstructions": path_obstructions,
                                            },
                                            "first_freshnel": {
                                                "obstructed": first_freshnel_obstruction,
                                                "message": first_freshnel_message,
                                            },
                                            "rx_signal_power": signal_power_line,
                                        }
                                    )

            except Exception as e:
                logger.error(f"Error during LOS prediction: {e}")
                raise RuntimeError(f"Error during LOS prediction: {e}")

    def coverage_prediction(self, request: CoveragePredictionRequest) -> bytes:
        logger.debug(f"Coverage prediction request: {request.json()}")

        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                logger.debug(f"Temporary directory created: {tmpdir}")

                # FIXME: Eventually support high-resolution terrain data
                request.high_resolution = False

                # Set hard limit of 100 km radius
                if request.radius > 100000:
                    logger.debug(
                        f"User tried to set radius of {request.radius} meters, setting to 100 km."
                    )
                    request.radius = 100000

                # determine the required terrain tiles
                required_tiles = Splat._calculate_required_terrain_tiles_coverage(
                    request.lat, request.lon, request.radius
                )

                # download and convert terrain tiles to SPLAT! sdf
                for tile_name, sdf_name, sdf_hd_name in required_tiles:
                    tile_data = self._download_terrain_tile(tile_name)
                    sdf_data = self._convert_hgt_to_sdf(
                        tile_data, tile_name, high_resolution=request.high_resolution
                    )

                    with open(
                        os.path.join(
                            tmpdir, sdf_hd_name if request.high_resolution else sdf_name
                        ),
                        "wb",
                    ) as sdf_file:
                        sdf_file.write(sdf_data)

                # write transmitter / qth file
                with open(os.path.join(tmpdir, "tx.qth"), "wb") as qth_file:
                    qth_file.write(
                        Splat._create_splat_qth(
                            "tx", request.lat, request.lon, request.tx_height
                        )
                    )

                # write model parameter / lrp file
                with open(os.path.join(tmpdir, "splat.lrp"), "wb") as lrp_file:
                    lrp_file.write(
                        Splat._create_splat_lrp(
                            ground_dielectric=request.ground_dielectric,
                            ground_conductivity=request.ground_conductivity,
                            atmosphere_bending=request.atmosphere_bending,
                            frequency_mhz=request.frequency_mhz,
                            radio_climate=request.radio_climate,
                            polarization=request.polarization,
                            situation_fraction=request.situation_fraction,
                            time_fraction=request.time_fraction,
                            tx_power=request.tx_power,
                            tx_gain=request.tx_gain,
                            system_loss=request.system_loss,
                        )
                    )

                # write colorbar / dcf file
                with open(os.path.join(tmpdir, "splat.dcf"), "wb") as dcf_file:
                    dcf_file.write(
                        Splat._create_splat_dcf(
                            colormap_name=request.colormap,
                            min_dbm=request.min_dbm,
                            max_dbm=request.max_dbm,
                        )
                    )

                logger.debug(f"Contents of {tmpdir}: {os.listdir(tmpdir)}")

                splat_command = [
                    (
                        self.splat_hd_binary
                        if request.high_resolution
                        else self.splat_binary
                    ),
                    "-t",
                    "tx.qth",
                    "-L",
                    str(request.rx_height),
                    "-metric",
                    "-R",
                    str(request.radius / 1000.0),
                    "-sc",
                    "-gc",
                    str(request.clutter_height),
                    "-ngs",
                    "-N",
                    "-o",
                    "output.ppm",
                    "-dbm",
                    "-db",
                    str(request.signal_threshold),
                    "-kml",
                    "-olditm",
                ]  # flag "olditm" uses the standard ITM model instead of ITWOM, which has produced unrealistic results.
                logger.debug(f"Executing SPLAT! command: {' '.join(splat_command)}")

                splat_result = subprocess.run(
                    splat_command,
                    cwd=tmpdir,
                    capture_output=True,
                    text=True,
                    check=False,
                )

                logger.debug(f"SPLAT! stdout:\n{splat_result.stdout}")
                logger.debug(f"SPLAT! stderr:\n{splat_result.stderr}")

                if splat_result.returncode != 0:
                    logger.error(
                        f"SPLAT! execution failed with return code {splat_result.returncode}"
                    )
                    raise RuntimeError(
                        f"SPLAT! execution failed with return code {splat_result.returncode}\n"
                        f"Stdout: {splat_result.stdout}\nStderr: {splat_result.stderr}"
                    )

                with open(os.path.join(tmpdir, "output.ppm"), "rb") as ppm_file:
                    with open(os.path.join(tmpdir, "output.kml"), "rb") as kml_file:
                        ppm_data = ppm_file.read()
                        kml_data = kml_file.read()
                        geotiff_data = Splat._create_splat_geotiff(
                            ppm_data,
                            kml_data,
                            request.colormap,
                            request.min_dbm,
                            request.max_dbm,
                        )

                logger.info("SPLAT! coverage prediction completed successfully.")
                return geotiff_data

            except Exception as e:
                logger.error(f"Error during coverage prediction: {e}")
                raise RuntimeError(f"Error during coverage prediction: {e}")

    @staticmethod
    def _calculate_required_terrain_tiles_los(
        tx_lat: float,
        tx_lon: float,
        rx_lat: float,
        rx_lon: float,
    ) -> List[Tuple[str, str, str]]:
        # For grid traversal, we treat longitude as the x-axis and latitude as the y-axis.
        x0, y0 = tx_lon, tx_lat
        x1, y1 = rx_lon, rx_lat

        # Compute differences in x and y direction.
        dx = x1 - x0
        dy = y1 - y0

        # Starting cell: we use floor to determine in which tile the start point lies.
        current_x = math.floor(x0)
        current_y = math.floor(y0)

        # Destination cell: the cell in which the receiver lies.
        dest_x = math.floor(x1)
        dest_y = math.floor(y1)

        # List of grid cells (each cell represented as (lat_tile, lon_tile)).
        grid_cells = [(current_y, current_x)]

        # Determine tDelta: the amount of "parametric time" to cross a grid cell in x or y.
        # Avoid division by zero for purely vertical or horizontal lines.
        tDeltaX = abs(1 / dx) if dx != 0 else float("inf")
        tDeltaY = abs(1 / dy) if dy != 0 else float("inf")

        # Determine the step direction and initial tMax values.
        if dx > 0:
            stepX = 1
            tMaxX = ((current_x + 1) - x0) / dx
        elif dx < 0:
            stepX = -1
            tMaxX = (x0 - current_x) / -dx
        else:
            stepX = 0
            tMaxX = float("inf")

        if dy > 0:
            stepY = 1
            tMaxY = ((current_y + 1) - y0) / dy
        elif dy < 0:
            stepY = -1
            tMaxY = (y0 - current_y) / -dy
        else:
            stepY = 0
            tMaxY = float("inf")

        # Traverse the grid until reaching the destination cell.
        while (current_x, current_y) != (dest_x, dest_y):
            if tMaxX < tMaxY:
                current_x += stepX
                tMaxX += tDeltaX
            else:
                current_y += stepY
                tMaxY += tDeltaY

            grid_cells.append((current_y, current_x))

        # Convert each grid cell coordinate to the tile naming convention.
        # The convention: N/S latitude with 2 digits and E/W longitude with 3 digits, e.g. N48E012.hgt.gz.
        tile_names = []
        for lat_tile, lon_tile in grid_cells:
            ns = "N" if lat_tile >= 0 else "S"
            ew = "E" if lon_tile >= 0 else "W"
            tile_name = f"{ns}{abs(lat_tile):02d}{ew}{abs(lon_tile):03d}.hgt.gz"
            sdf_filename = Splat._hgt_filename_to_sdf_filename(
                tile_name, high_resolution=False
            )
            sdf_hd_filename = Splat._hgt_filename_to_sdf_filename(
                tile_name, high_resolution=True
            )
            tile_names.append((tile_name, sdf_filename, sdf_hd_filename))

        logger.debug(
            "Required terrain tile names (optimized for line-of-sight): %s", tile_names
        )
        return tile_names

    @staticmethod
    def _calculate_required_terrain_tiles_coverage(
        lat: float, lon: float, radius: float
    ) -> List[Tuple[str, str, str]]:
        earth_radius = 6378137  # meters, approximate.

        # Convert radius to angular distance in degrees
        delta_deg = (radius / earth_radius) * (180 / math.pi)

        # Compute bounding box in degrees
        lat_min = lat - delta_deg
        lat_max = lat + delta_deg
        lon_min = lon - delta_deg / math.cos(math.radians(lat))
        lon_max = lon + delta_deg / math.cos(math.radians(lat))

        # Determine tile boundaries (rounded to 1-degree tiles)
        lat_min_tile = math.floor(lat_min)
        lat_max_tile = math.floor(lat_max)
        lon_min_tile = math.floor(lon_min)
        lon_max_tile = math.floor(lon_max)

        # All tile names within the bounding box
        tile_names = []

        for lat_tile in range(lat_min_tile, lat_max_tile + 1):
            for lon_tile in range(lon_min_tile, lon_max_tile + 1):
                ns = "N" if lat_tile >= 0 else "S"
                ew = "E" if lon_tile >= 0 else "W"
                tile_name = f"{ns}{abs(lat_tile):02d}{ew}{abs(lon_tile):03d}.hgt.gz"

                # .sdf file boundaries
                lat_start = lat_tile
                lon_start = lon_tile
                lat_end = lat_start + 1
                lon_end = lon_start + 1

                # Generate .sdf file names
                sdf_filename = Splat._hgt_filename_to_sdf_filename(
                    tile_name, high_resolution=False
                )
                sdf_hd_filename = Splat._hgt_filename_to_sdf_filename(
                    tile_name, high_resolution=True
                )
                tile_names.append((tile_name, sdf_filename, sdf_hd_filename))

        logger.debug("required tile names are: ")
        logger.debug(tile_names)
        return tile_names

    @staticmethod
    def _download_convert_tiles(
        self,
        required_tiles: List[Tuple[str, str, str]],
        high_resolution: bool,
        tmpdir: str,
    ) -> None:
        # download and convert terrain tiles to SPLAT! sdf
        for tile_name, sdf_name, sdf_hd_name in required_tiles:
            tile_data = self._download_terrain_tile(tile_name)
            sdf_data = self._convert_hgt_to_sdf(
                tile_data,
                tile_name,
                high_resolution=high_resolution,
            )

            with open(
                os.path.join(
                    tmpdir,
                    sdf_hd_name if high_resolution else sdf_name,
                ),
                "wb",
            ) as sdf_file:
                sdf_file.write(sdf_data)

    @staticmethod
    def _create_splat_qth(
        name: str, latitude: float, longitude: float, elevation: float
    ) -> bytes:
        logger.debug(f"Generating .qth file content for site '{name}'.")

        try:
            # Create the .qth file content
            contents = (
                f"{name}\n"
                f"{latitude:.6f}\n"
                f"{abs(longitude) if longitude < 0 else 360 - longitude:.6f}\n"  # SPLAT! expects west longitude as a positive number.
                f"{elevation:.2f}\n"
            )
            logger.debug(f"Generated .qth file contents:\n{contents}")
            return contents.encode("utf-8")  # Return as bytes
        except Exception as e:
            logger.error(f"Error generating .qth file content: {e}")
            raise ValueError(f"Failed to generate .qth content: {e}")

    @staticmethod
    def _create_splat_lrp(
        ground_dielectric: float,
        ground_conductivity: float,
        atmosphere_bending: float,
        frequency_mhz: float,
        radio_climate: Literal[
            "equatorial",
            "continental_subtropical",
            "maritime_subtropical",
            "desert",
            "continental_temperate",
            "maritime_temperate_land",
            "maritime_temperate_sea",
        ],
        polarization: Literal["horizontal", "vertical"],
        situation_fraction: float,
        time_fraction: float,
        tx_power: float,
        tx_gain: float,
        system_loss: float,
    ) -> bytes:
        logger.debug("Generating .lrp file content.")

        # Mapping for radio climate and polarization to SPLAT! enumerations
        climate_map = {
            "equatorial": 1,
            "continental_subtropical": 2,
            "maritime_subtropical": 3,
            "desert": 4,
            "continental_temperate": 5,
            "maritime_temperate_land": 6,
            "maritime_temperate_sea": 7,
        }
        polarization_map = {"horizontal": 0, "vertical": 1}

        # Calculate ERP in Watts
        erp_watts = 10 ** ((tx_power + tx_gain - system_loss - 30) / 10)
        logger.debug(
            f"Calculated ERP in Watts: {erp_watts:.2f} "
            f"(tx_power={tx_power}, tx_gain={tx_gain}, system_loss={system_loss})"
        )

        # Generate the content, maintaining the SPLAT! format
        try:
            contents = (
                f"{ground_dielectric:.3f}  ; Earth Dielectric Constant\n"
                f"{ground_conductivity:.6f}  ; Earth Conductivity\n"
                f"{atmosphere_bending:.3f}  ; Atmospheric Bending Constant\n"
                f"{frequency_mhz:.3f}  ; Frequency in MHz\n"
                f"{climate_map[radio_climate]}  ; Radio Climate\n"
                f"{polarization_map[polarization]}  ; Polarization\n"
                f"{situation_fraction / 100.0:.2f} ; Fraction of situations\n"
                f"{time_fraction / 100.0:.2f}  ; Fraction of time\n"
                f"{erp_watts:.2f}  ; ERP in Watts\n"
            )
            logger.debug(f"Generated .lrp file contents:\n{contents}")
            return contents.encode("utf-8")  # Return as bytes
        except Exception as e:
            logger.error(f"Error generating .lrp file content: {e}")
            raise

    @staticmethod
    def _create_splat_dcf(colormap_name: str, min_dbm: float, max_dbm: float) -> bytes:
        logger.debug(
            f"Generating .dcf file content using colormap '{colormap_name}', min_dbm={min_dbm}, max_dbm={max_dbm}."
        )

        try:
            # Generate color map values and normalization
            cmap = plt.get_cmap(colormap_name)
            cmap_values = np.linspace(
                max_dbm, min_dbm, 32
            )  # SPLAT! supports up to 32 levels
            cmap_norm = plt.Normalize(vmin=min_dbm, vmax=max_dbm)

            # Generate RGB values
            rgb_colors = (cmap(cmap_norm(cmap_values))[:, :3] * 255).astype(int)

            # Prepare .dcf content
            contents = "; SPLAT! Auto-generated DBM Signal Level Color Definition\n;\n"
            contents += "; Format: dBm: red, green, blue\n;\n"
            for value, rgb in zip(cmap_values, rgb_colors):
                contents += f"{int(value):+4d}: {rgb[0]:3d}, {rgb[1]:3d}, {rgb[2]:3d}\n"

            logger.debug(f"Generated .dcf file contents:\n{contents}")
            return contents.encode("utf-8")

        except Exception as e:
            logger.error(f"Error generating .dcf file content: {e}")
            raise ValueError(f"Failed to generate .dcf content: {e}")

    @staticmethod
    def create_splat_colorbar(
        colormap_name: str,
        min_dbm: float,
        max_dbm: float,
    ) -> list:
        cmap = plt.get_cmap(colormap_name, 256)  # colormap with 256 levels
        cmap_norm = plt.Normalize(
            vmin=min_dbm, vmax=max_dbm
        )  # Normalize based on dBm range
        cmap_values = np.linspace(min_dbm, max_dbm, 255)

        # Map data values to RGB for visible colors
        rgb_colors = list(cmap(cmap_norm(cmap_values))[:, :3] * 255).astype(int)
        return rgb_colors

    @staticmethod
    def _create_splat_geotiff(
        ppm_bytes: bytes,
        kml_bytes: bytes,
        colormap_name: str,
        min_dbm: float,
        max_dbm: float,
        null_value: int = 255,  # Define the null value for transparency
    ) -> bytes:
        logger.info("Starting GeoTIFF generation from SPLAT! PPM and KML data.")

        try:
            # Parse KML and extract bounding box
            logger.debug("Parsing KML content.")
            tree = ET.ElementTree(ET.fromstring(kml_bytes))
            namespace = {"kml": "http://earth.google.com/kml/2.1"}
            box = tree.find(".//kml:LatLonBox", namespace)

            north = float(box.find("kml:north", namespace).text)
            south = float(box.find("kml:south", namespace).text)
            east = float(box.find("kml:east", namespace).text)
            west = float(box.find("kml:west", namespace).text)

            logger.debug(
                f"Extracted bounding box: north={north}, south={south}, east={east}, west={west}"
            )

            # Read PPM content
            logger.debug("Reading PPM content.")
            with Image.open(io.BytesIO(ppm_bytes)) as img:
                img_array = np.array(
                    img.convert("L")
                )  # Convert to single-channel grayscale
                img_array = np.clip(img_array, 0, 255).astype("uint8")

            logger.debug(f"PPM image dimensions: {img_array.shape}")

            # Mask null values
            img_array = np.where(
                img_array == null_value, 255, img_array
            )  # Optionally set to 0
            no_data_value = null_value

            # Create GeoTIFF using Rasterio
            height, width = img_array.shape
            transform = from_bounds(west, south, east, north, width, height)
            logger.debug(f"GeoTIFF transform matrix: {transform}")

            # Generate colormap with transparency
            cmap = plt.get_cmap(colormap_name, 256)  # colormap with 256 levels
            cmap_norm = plt.Normalize(
                vmin=min_dbm, vmax=max_dbm
            )  # Normalize based on dBm range
            cmap_values = np.linspace(min_dbm, max_dbm, 255)

            # Map data values to RGB for visible colors
            rgb_colors = (cmap(cmap_norm(cmap_values))[:, :3] * 255).astype(int)

            # Initialize GDAL-compatible colormap with transparency for null values
            gdal_colormap = {i: tuple(rgb) + (255,) for i, rgb in enumerate(rgb_colors)}

            # Write GeoTIFF to memory
            with io.BytesIO() as buffer:
                with rasterio.open(
                    buffer,
                    "w",
                    driver="GTiff",
                    height=height,
                    width=width,
                    count=1,  # Single-band data
                    dtype="uint8",
                    crs="EPSG:4326",
                    transform=transform,
                    photometric="palette",  # Colormap interpretation
                    compress="lzw",
                    nodata=no_data_value,  # Set NoData value
                ) as dst:
                    dst.write(img_array, 1)  # Write the raster data
                    dst.write_colormap(1, gdal_colormap)  # Attach the colormap

                buffer.seek(0)
                geotiff_bytes = buffer.read()

            logger.info("GeoTIFF generation successful.")
            return geotiff_bytes

        except Exception as e:
            logger.error(f"Error during GeoTIFF generation: {e}")
            raise RuntimeError(f"Error during GeoTIFF generation: {e}")

    def _download_terrain_tile(self, tile_name: str) -> bytes:
        if tile_name in self.tile_cache:
            logger.info(f"Cache hit: {tile_name} found in the local cache.")
            return self.tile_cache[tile_name]

        # Download the tile from S3 if not in cache
        tile_dir_prefix = tile_name[:3]
        s3_key = f"{self.bucket_prefix}/{tile_dir_prefix}/{tile_name}"
        logger.info(f"Downloading {tile_name} from {self.bucket_name}/{s3_key}...")
        try:
            obj = self.s3.get_object(Bucket=self.bucket_name, Key=s3_key)
            tile_data = obj["Body"].read()
            # Store the tile in the cache
            self.tile_cache[tile_name] = tile_data
            return tile_data
        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchKey":
                logger.info(
                    f"Tile {tile_name} not found in S3 bucket, trying to download V1 SRTM data instead: {e}"
                )
                s3_key = f"skadi/{tile_dir_prefix}/{tile_name}"
                obj = self.s3.get_object(Bucket=self.bucket_name, Key=s3_key)
                tile_data = obj["Body"].read()
                # Store the tile in the cache
                self.tile_cache[tile_name] = tile_data
                return tile_data
            else:
                logger.error(
                    f"Failed to download {tile_name} from S3 due to ClientError: {e}"
                )
                raise
        except Exception as e:
            logger.error(f"Failed to download {tile_name} from S3: {e}")
            raise

    @staticmethod
    def _hgt_filename_to_sdf_filename(
        hgt_filename: str, high_resolution: bool = False
    ) -> str:
        lat = int(hgt_filename[1:3]) * (1 if hgt_filename[0] == "N" else -1)
        min_lon = int(hgt_filename[4:7]) - (
            -1 if hgt_filename[3] == "E" else 1
        )  # fix off-by-one error in eastern hemisphere
        min_lon = 360 - min_lon if hgt_filename[3] == "E" else min_lon
        max_lon = 0 if min_lon == 359 else min_lon + 1
        return f"{lat}:{lat + 1}:{min_lon}:{max_lon}{'-hd.sdf' if high_resolution else '.sdf'}"

    def _convert_hgt_to_sdf(
        self, tile: bytes, tile_name: str, high_resolution: bool = False
    ) -> bytes:
        sdf_filename = Splat._hgt_filename_to_sdf_filename(tile_name, high_resolution)

        # Check cache for converted file
        if sdf_filename in self.tile_cache:
            logger.info(f"Cache hit: {sdf_filename} found in the local cache.")
            return self.tile_cache[sdf_filename]

        # Create temporary working directory
        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                # Decompress the tile into the temporary directory
                hgt_path = os.path.join(tmpdir, tile_name.replace(".gz", ""))
                logger.info(f"Decompressing {tile_name} into {hgt_path}.")
                with gzip.GzipFile(fileobj=io.BytesIO(tile)) as gz_file:
                    with open(hgt_path, "wb") as hgt_file:
                        hgt_file.write(gz_file.read())

                # Downsample to 3-arcsecond resolution if not in high-resolution mode
                if not high_resolution:
                    try:
                        logger.info(
                            f"Downsampling {hgt_path} to 3-arcsecond resolution."
                        )
                        with rasterio.open(hgt_path) as src:
                            # Apply a scaling factor to transform for 3-arcsecond resolution
                            scale_factor = (
                                3  # 3-arcsecond is 3 times coarser than 1-arcsecond
                            )
                            transform = src.transform * Affine.scale(
                                scale_factor, scale_factor
                            )

                            # Resample data to 3-arcsecond resolution
                            data = src.read(
                                # 3-arcsecond SRTM tiles always have dimensions of 1201x1201 pixels.
                                out_shape=(
                                    src.count,  # Number of bands
                                    1201,  # Downsampled height
                                    1201,  # Downsampled width
                                ),
                                resampling=Resampling.average,
                            )

                            # Update metadata for the new dataset
                            meta = src.meta.copy()
                            meta.update(
                                {
                                    "transform": transform,
                                    "width": 1201,
                                    "height": 1201,
                                }
                            )

                        # Overwrite the temporary file with downsampled data
                        with rasterio.open(hgt_path, "w", **meta) as dst:
                            dst.write(data)

                        logger.info(f"Successfully downsampled {hgt_path}.")
                    except Exception as e:
                        logger.error(f"Failed to downsample {hgt_path}: {e}")
                        raise RuntimeError(f"Downsampling error for {hgt_path}: {e}")

                # Call srtm2sdf or srtm2sdf-hd in the temporary directory
                cmd = (
                    self.srtm2sdf_hd_binary if high_resolution else self.srtm2sdf_binary
                )
                logger.info(f"Converting {hgt_path} to {sdf_filename} using {cmd}.")
                result = subprocess.run(
                    [cmd, os.path.basename(tile_name.replace(".gz", ""))],
                    cwd=tmpdir,
                    capture_output=True,
                    text=True,
                    check=True,
                )

                logger.debug(f"srtm2sdf output:\n{result.stderr}")
                sdf_path = os.path.join(tmpdir, sdf_filename)

                # Ensure the .sdf file was created
                if not os.path.exists(sdf_path):
                    logger.error(f"Expected .sdf file not found: {sdf_path}")
                    raise RuntimeError(f"Failed to generate .sdf file: {sdf_path}")

                # Read and cache the .sdf file
                with open(sdf_path, "rb") as sdf_file:
                    sdf_data = sdf_file.read()
                self.tile_cache[sdf_filename] = sdf_data

                logger.info(f"Successfully converted and cached {sdf_filename}.")
                return sdf_data

            except subprocess.CalledProcessError as e:
                logger.error(f"Subprocess error during conversion of {tile_name}: {e}")
                logger.error(f"stderr: {e.stderr}")
                raise RuntimeError(
                    f"Subprocess error during conversion of {tile_name}: {e}"
                )

            except Exception as e:
                logger.error(
                    f"Error during conversion of {tile_name} to {sdf_filename}: {e}"
                )
                raise RuntimeError(f"Conversion error for {tile_name}: {e}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    try:
        splat_service = Splat(
            splat_path="",  # Replace with the actual SPLAT! binary path
        )

        # Create a test coverage prediction request
        test_coverage_request = CoveragePredictionRequest(
            lat=51.4408448,
            lon=-0.8994816,
            tx_height=1.0,
            ground_dielectric=15.0,
            ground_conductivity=0.005,
            atmosphere_bending=301.0,
            frequency_mhz=868.0,
            radio_climate="continental_temperate",
            polarization="vertical",
            situation_fraction=95.0,
            time_fraction=95.0,
            tx_power=30.0,
            tx_gain=1.0,
            system_loss=2.0,
            rx_height=1.0,
            radius=50000.0,
            colormap="CMRmap",
            min_dbm=-130.0,
            max_dbm=-80.0,
            signal_threshold=-130.0,
            high_resolution=False,
        )

        # Execute coverage prediction
        logger.info("Starting SPLAT! coverage prediction...")
        result = splat_service.coverage_prediction(test_coverage_request)

        # Save GeoTIFF output for inspection
        output_path = "splat_output.tif"
        with open(output_path, "wb") as output_file:
            output_file.write(result)
        logger.info(f"GeoTIFF saved to: {output_path}")

    except Exception as e:
        logger.error(f"Error during SPLAT! test: {e}")
        raise
