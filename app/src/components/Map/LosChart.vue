<template>
  <MglCustomControl v-if="store.losSimModeData.chart.show" :position="props.position">
    <div :class="['bg-white border rounded shadow-lg', hide ? 'border-gray-100' : 'border-gray-300']">
      <Button v-if="hide" text="Show" @click="hide = false" class="px-2! m-2 w-auto! bg-orange-400!" />
      <div v-if="!hide">
        <ApexCharts :width="isMobileDevice() ? '100%' : '400'" height="250" type="line"
          :series="store.losSimModeData.chart.data" :options="store.losSimModeData.chart.options" />
        <div class="flex items-center justify-between bg-white p-2 border-t border-gray-300">
          <div class="text-black ml-1">
            <p><b>Path Loss: </b>{{ store.losSimModeData.chart.path_loss }} dB</p>
            <p><b>Longley-Rice Loss: </b>{{ store.losSimModeData.chart.longley_rice_loss }} dB</p>
            <p><b>Expected RX RSSI: </b>{{ store.losSimModeData.chart.rx_signal_power }} dBm</p>
            <b>{{ store.losSimModeData.chart.path.obstructed ? "LOS is Obstructed" : "LOS is Unobstructed" }}</b>
          </div>
          <Button text="Hide" @click="hide = true" class="px-2! py-3 w-auto! bg-orange-400!" />
        </div>
      </div>
    </div>
  </MglCustomControl>
</template>
<script setup lang="ts">
import { MglCustomControl } from "@indoorequal/vue-maplibre-gl";
import type { ControlPosition } from "maplibre-gl";
import VueApexCharts from "vue3-apexcharts";
import { useStore } from "../../stores/store";
import { isMobileDevice } from "../../utils";
import Button from "../Inputs/Button.vue";
import { ref } from "vue";

// vue3-apexcharts exposes the Vue component; the core apexcharts package is non-Vue and was causing runtime errors
const ApexCharts = VueApexCharts;

export type LayerSelectorProps = {
  position: ControlPosition | undefined;
};

const hide = ref(false);

const props = defineProps<LayerSelectorProps>();

const store = useStore();
</script>
<style>
.apexcharts-tooltip {
  color: #000 !important;
}
</style>
