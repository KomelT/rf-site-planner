<template>
  <MglCustomControl v-if="store.chart.show" :position="props.position">
    <VueApexCharts width="400" height="250" type="line" :series="store.chart.data" :options="store.chart.options" />
  </MglCustomControl>
</template>
<script setup lang="ts">
import { MglCustomControl } from "@indoorequal/vue-maplibre-gl";
import type { ControlPosition } from "maplibre-gl";
import VueApexCharts from "vue3-apexcharts";
import { useStore } from "../../stores/store";

export type LayerSelectorProps = {
	position: ControlPosition | undefined;
};

const props = defineProps<LayerSelectorProps>();

const store = useStore();
</script>