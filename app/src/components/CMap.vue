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
	MglLineLayer
} from "@indoorequal/vue-maplibre-gl";
import { computed, ref } from "vue";
import { useStore } from "../stores/store";
import CentralNodeTable from "./Map/CentralNodeTable.vue";
import LayerSelectorControl from "./Map/LayerSelectorControl.vue";
import LosChart from "./Map/LosChart.vue";
import CoverageLegend from "./Map/CoverageLegend.vue";

const store = useStore();

const mapStyle = computed(() => {
	return `/map-styles/${store.mapStyle}.json`;
});

const layout: {
	"line-join": DataDrivenPropertyValueSpecification<"round" | "miter" | "bevel"> | undefined,
	"line-cap": PropertyValueSpecification<"round" | "butt" | "square"> | undefined
} = {
	'line-join': "round",
	'line-cap': "round"
};

const paint = {
	'line-color': '#FF0000',
	'line-width': 3
};

import { watch } from "vue";
import { DataDrivenPropertyValueSpecification, PropertyValueSpecification } from "maplibre-gl";

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

// Watch for changes in the coordinates
watch(() => store.geoJsonLine.coordinates, (newCoordinates) => {
	geojson.value.features[0].geometry.coordinates = newCoordinates;
	geojson.value = { ...geojson.value };
}, { deep: true, immediate: true });
</script>
<style>
.maplibregl-map {
	height: calc(100vh - 64px) !important;
}
</style>