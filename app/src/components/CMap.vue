<template>
  <MglMap :mapStyle="mapStyle" :center="mapDefaultCenter" :zoom="mapDefaultZoom">
    <MglNavigationControl position="top-left" />
  </MglMap>
</template>
<script setup lang="ts">
import 'maplibre-gl/dist/maplibre-gl.css';
import { MglMap, MglNavigationControl } from '@indoorequal/vue-maplibre-gl';

const mapStyle =
  "https://raw.githubusercontent.com/hc-oss/maplibre-gl-styles/master/styles/osm-mapnik/v8/default.json";
const mapDefaultCenter = [13.75, 45.84] as [
  number,
  number,
];
const mapDefaultZoom = 12;
</script>
<style>
.maplibregl-map {
  height: calc(100vh - 64px) !important;
}
</style>