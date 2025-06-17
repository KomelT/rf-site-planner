<template>
  <MglCustomControl v-if="store.chart.show" :position="props.position">
    <VueApexCharts width="400" height="250" type="line" :series="store.chart.data" :options="store.chart.options" />
    <div class="text-black ml-5">
      <p><b>RX signal power: </b>{{ store.chart.rx_signal_power }} dBm</p>
      <b>{{ store.chart.path.obstructed ? "LOS is Obstructed" : "LOS is Unobstructed" }}</b>
    </div>
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
<style>
.apexcharts-tooltip {
  color: #000 !important;
}
</style>