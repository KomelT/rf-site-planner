<template>
	<MglMap :mapStyle="mapStyle" :center="[13.726414891504586, 45.85477731775239]" :zoom="12">
		<MglNavigationControl position="top-left" />
		<MglGeolocateControl position="top-left" />
		<LayerSelectorControl position="top-right" />
		<LosChart position="top-right" />
		<CentralNodeTable position="top-right" />
		<CoverageLegend position="bottom-right" />
		<MglGeoJsonSource source-id="geojson" :data="geojson as GeoJSON.GeoJSON">
			<MglLineLayer layer-id="geojson" :layout="layout" :paint="paint" />
		</MglGeoJsonSource>
	</MglMap>
</template>
<script setup lang="ts">
import "maplibre-gl/dist/maplibre-gl.css";
import {
	MglGeolocateControl,
	MglMap,
	MglNavigationControl,
	MglGeoJsonSource,
	MglLineLayer,
	useMap
} from "@indoorequal/vue-maplibre-gl";
import { Ref, ref, watch } from "vue";
import { DataDrivenPropertyValueSpecification, PropertyValueSpecification, StyleSpecification } from "maplibre-gl";
import { useStore } from "../stores/store";
import CentralNodeTable from "./Map/CentralNodeTable.vue";
import LosChart from "./Map/LosChart.vue";
import CoverageLegend from "./Map/CoverageLegend.vue";
import LayerSelectorControl from "./Map/LayerSelectorControl.vue";

const store = useStore();
const map = useMap();

const mapStyle: Ref<StyleSpecification> = ref(
	{
		"version": 8,
		"name": "OpenStreetMap raster tiles",
		"sources": {
			"basemap": {
				"type": "raster",
				"tiles": ["https://a.tile.openstreetmap.org/{z}/{x}/{y}.png"],
				"tileSize": 256,
				"attribution": "Basemap <a href='https://www.openstreetmap.org' target=_blank>©  OpenStreetMap contributors</a>"
			}
		},
		"layers": [
			{
				"id": "background",
				"type": "background",
				"paint": {
					"background-color": "rgba(0,0,0,0)"
				}
			},
			{
				"id": "basemap",
				"type": "raster",
				"source": "basemap"
			}
		]
	}

);

watch(() => store.mapStyle, (newStyle) => {
	let tmpStyle = map.map?.getStyle();
	if (!tmpStyle) return;

	switch (newStyle) {
		case "openstreetmap":
			tmpStyle.sources.basemap.tiles[0] = "https://a.tile.openstreetmap.org/{z}/{x}/{y}.png";
			tmpStyle.sources.basemap.attribution = "Basemap <a href='https://www.openstreetmap.org' target=_blank>©  OpenStreetMap contributors</a>";
			break;
		case "opentopomap":
			tmpStyle.sources.basemap.tiles[0] = "https://a.tile.opentopomap.org/{z}/{x}/{y}.png";
			tmpStyle.sources.basemap.attribution = "Basemap data <a href='https://www.openstreetmap.org' target=_blank>©  OpenStreetMap contributors</a> | Basemap style <a href='https://www.opentopomap.org' target=_blank>©  OpenTopoMap contributors</a>";
			break;
		case "satellite":
			tmpStyle.sources.basemap.tiles[0] = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}";
			tmpStyle.sources.basemap.attribution = "Basemap <a href='https://developers.arcgis.com/documentation/mapping-apis-and-services/deployment/basemap-attribution/' target=_blank>© Esri</a>";
			break;
		default:
			tmpStyle.sources.basemap.tiles[0] = "https://a.tile.openstreetmap.org/{z}/{x}/{y}.png";
			tmpStyle.sources.basemap.attribution = "Basemap <a href='https://www.openstreetmap.org' target=_blank>©  OpenStreetMap contributors</a>";
	}

	map.map?.setStyle(tmpStyle);
}, { immediate: true });

const layout: {
	"line-join": DataDrivenPropertyValueSpecification<"round" | "miter" | "bevel"> | undefined,
	"line-cap": PropertyValueSpecification<"round" | "butt" | "square"> | undefined
} = {
	"line-join": "round",
	"line-cap": "round"
};

const paint = {
	"line-color": "#FF0000",
	"line-width": 3
};

const geojson = ref({
	type: "FeatureCollection",
	features: [
		{
			type: "Feature",
			properties: {},
			geometry: {
				type: "LineString",
				coordinates: store.geoJsonLine.coordinates
			}
		}
	]
});

// Keep GeoJSON layer in sync with store coordinates
watch(
	() => store.geoJsonLine.coordinates,
	(newCoordinates) => {
		geojson.value.features[0].geometry.coordinates = newCoordinates;
		geojson.value = { ...geojson.value };
	},
	{ deep: true, immediate: true },
);
</script>
<style>
.maplibregl-map {
	height: calc(100vh - 64px) !important;
}
</style>
