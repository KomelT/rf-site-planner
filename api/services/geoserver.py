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
            timeout=15,
        )

        if req.status_code != 201:
            logger.error(f"Failed to upload GeoTIFF to Geoserver: {req.status_code}")
            raise Exception(f"Failed to upload GeoTIFF to Geoserver: {req.status_code}")

        logger.info(f"Storing result in Geoserver for task {task_id}")
        
        # Create and assign a raster style for proper WMS rendering
        _create_raster_style_if_missing()
        _assign_style_to_coverage(task_id, "raster-coverage")
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
            timeout=15,
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



def _create_raster_style_if_missing():
    """Create a default raster style in GeoServer if it doesn't exist."""
    try:
        # Check if style exists
        check_req = requests.get(
            "http://geoserver:8080/geoserver/rest/styles/raster-coverage.json",
            auth=(
                getenv("GEOSERVER_ADMIN_USER"),
                getenv("GEOSERVER_ADMIN_PASSWORD"),
            ),
            timeout=15,
        )
        
        if check_req.status_code == 200:
            logger.info("Raster style 'raster-coverage' already exists")
            return
        
        # Create simple rasterize SLD for rendering coverage with embedded colormap
        sld_body = """<?xml version="1.0" encoding="ISO-8859-1"?>
<StyledLayerDescriptor version="1.0.0"
    xsi:schemaLocation="http://www.opengis.net/sld StyledLayerDescriptor.xsd"
    xmlns="http://www.opengis.net/sld"
    xmlns:ogc="http://www.opengis.net/ogc"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <NamedLayer>
        <Name>raster-coverage</Name>
        <UserStyle>
            <Title>Raster Coverage Default Style</Title>
            <FeatureTypeStyle>
                <Transformation>
                    <ogc:Function name="ras:Colormap">
                        <ogc:Function name="parameter">
                            <ogc:Literal>data</ogc:Literal>
                        </ogc:Function>
                        <ogc:Literal>FLOAT32</ogc:Literal>
                        <ogc:Literal>0</ogc:Literal>
                        <ogc:Function name="parameter">
                            <ogc:Literal>outputType</ogc:Literal>
                            <ogc:Literal>RGBA</ogc:Literal>
                        </ogc:Function>
                    </ogc:Function>
                </Transformation>
                <Rule>
                    <RasterSymbolizer />
                </Rule>
            </FeatureTypeStyle>
        </UserStyle>
    </NamedLayer>
</StyledLayerDescriptor>"""
        
        create_req = requests.post(
            "http://geoserver:8080/geoserver/rest/styles",
            auth=(
                getenv("GEOSERVER_ADMIN_USER"),
                getenv("GEOSERVER_ADMIN_PASSWORD"),
            ),
            headers={"Content-Type": "application/vnd.ogc.sld+xml"},
            params={"name": "raster-coverage"},
            data=sld_body,
            timeout=15,
        )
        
        if create_req.status_code != 201:
            logger.error(f"Failed to create raster style: {create_req.status_code}")
            logger.error(f"Response: {create_req.text}")
        else:
            logger.info("Raster style 'raster-coverage' created successfully")
            
    except Exception as e:
        logger.error(f"Error creating raster style: {e}")


def _assign_style_to_coverage(task_id: str, style_name: str):
    """Assign a default style to a coverage layer."""
    try:
        # Get current coverage metadata
        get_req = requests.get(
            f"http://geoserver:8080/geoserver/rest/workspaces/RF-SITE-PLANNER/coveragestores/{task_id}/coverages/{task_id}.json",
            auth=(
                getenv("GEOSERVER_ADMIN_USER"),
                getenv("GEOSERVER_ADMIN_PASSWORD"),
            ),
            timeout=15,
        )
        
        if get_req.status_code != 200:
            logger.error(f"Failed to get coverage info: {get_req.status_code}")
            return
        
        coverage_data = get_req.json()
        
        # Set default style
        if "coverage" in coverage_data:
            coverage_data["coverage"]["defaultStyle"] = {
                "name": style_name,
                "href": f"http://geoserver:8080/geoserver/rest/styles/{style_name}.json"
            }
            
            # Update and commit
            update_req = requests.put(
                f"http://geoserver:8080/geoserver/rest/workspaces/RF-SITE-PLANNER/coveragestores/{task_id}/coverages/{task_id}.json",
                auth=(
                    getenv("GEOSERVER_ADMIN_USER"),
                    getenv("GEOSERVER_ADMIN_PASSWORD"),
                ),
                headers={"Content-Type": "application/json"},
                json=coverage_data,
                timeout=15,
            )
            
            if update_req.status_code in [200, 201]:
                logger.info(f"Style '{style_name}' assigned to coverage {task_id}")
            else:
                logger.error(f"Failed to assign style: {update_req.status_code}")
                logger.error(f"Response: {update_req.text}")
        
    except Exception as e:
        logger.error(f"Error assigning style to coverage: {e}")
