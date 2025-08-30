import os
from io import BytesIO
from logging import INFO, basicConfig, getLogger
from os import getenv

import requests

basicConfig(level=INFO)
logger = getLogger(__name__)


def store_tiff_in_geoserver(task_id: str, geotiff_data: bytes):
    try:
        with open(f"/var/app/geoserver_data/{task_id}.geotiff", "wb") as tiff_file:
            tiff_file.write(BytesIO(geotiff_data).read())
            logger.info(f"GeoTIFF saved to /var/app/geoserver_data/{task_id}.geotiff")

        # https://docs.geoserver.org/main/en/user/rest/api/coveragestores.html#workspaces-ws-coveragestores-format
        req = requests.request(
            "PUT",
            f"http://geoserver:8080/geoserver/rest/workspaces/RF-SITE-PLANNER/coveragestores/{task_id}/external.geotiff?configure=first&coverageName={task_id}",
            auth=(
                getenv("GEOSERVER_ADMIN_USER"),
                getenv("GEOSERVER_ADMIN_PASSWORD"),
            ),
            headers={"Content-type": "text/plain"},
            data=f"/opt/geoserver_data/data/{task_id}.geotiff",
        )

        if req.status_code != 201:
            logger.error(f"Failed to upload GeoTIFF to Geoserver: {req.status_code}")
            raise Exception(f"Failed to upload GeoTIFF to Geoserver: {req.status_code}")

        logger.info(f"Storing result in Geoserver for task {task_id}")
    except Exception as e:
        logger.error(
            f"Unexpected error while storing GeoTIFF data for task {task_id}: {e}"
        )
        raise


def remove_tiff_from_geoserver(task_id: str):
    try:
        # https://docs.geoserver.org/main/en/user/rest/api/coveragestores.html#workspaces-ws-coveragestores-cs-format
        req = requests.request(
            "DELETE",
            f"http://geoserver:8080/geoserver/rest/workspaces/RF-SITE-PLANNER/coveragestores/{task_id}.geotiff?purge=all&recurse=true",
            auth=(
                getenv("GEOSERVER_ADMIN_USER"),
                getenv("GEOSERVER_ADMIN_PASSWORD"),
            ),
        )

        os.remove(f"/var/app/geoserver_data/{task_id}.geotiff")

        if req.status_code != 200:
            logger.error(f"Failed to remove GeoTIFF from Geoserver: {req.status_code}")
            raise Exception(
                f"Failed to remove GeoTIFF from Geoserver: {req.status_code}"
            )

        logger.info(f"Removed GeoTIFF from Geoserver for task {task_id}")
    except Exception as e:
        logger.error(
            f"Unexpected error while removing GeoTIFF data for task {task_id}: {e}"
        )
