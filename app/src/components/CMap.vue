<template>
	<MglMap :mapStyle="mapStyle" :center="[13.726414891504586, 45.85477731775239]" :zoom="12">
		<MglNavigationControl position="top-left" />
		<MglGeolocateControl position="top-left" />
		<LayerSelectorControl position="top-right" />
		<LosChart position="top-right" />
	</MglMap>
</template>
<script setup lang="ts">
import "maplibre-gl/dist/maplibre-gl.css";
import {
	MglGeolocateControl,
	MglMap,
	MglNavigationControl,
} from "@indoorequal/vue-maplibre-gl";
import { computed } from "vue";
import { useStore } from "../stores/store";
import LayerSelectorControl from "./Map/LayerSelectorControl.vue";
import LosChart from "./Map/LosChart.vue";

const store = useStore();

const mapStyle = computed(() => {
	return `/map-styles/${store.mapStyle}.json`;
});
</script>
<style>
.maplibregl-map {
	height: calc(100vh - 64px) !important;
}
</style>