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

        body = f"/opt/geoserver_data/data/{task_id}.geotiff"
        req = requests.request(
            "PUT",
            f"http://geoserver:8080/geoserver/rest/workspaces/RF-SITE-PLANNER/coveragestores/{task_id}/external.geotiff?configure=first&coverageName={task_id}",
            auth=(
                getenv("GEOSERVER_ADMIN_USER"),
                getenv("GEOSERVER_ADMIN_PASSWORD"),
            ),
            headers={"Content-type": "text/plain"},
            data=body,
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
