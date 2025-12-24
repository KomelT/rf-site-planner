<template>
  <MglCustomControl :position="props.position">
    <div v-if="!openOptions" class="bg-white rounded-lg shadow-md" @mouseenter="() => openOptions = true">
      <img src="/layers.png" alt="Layers" class="w-7 h-7 p-2 box-content" />
    </div>
    <div v-if="openOptions" class="w-36 p-2 bg-red text-gray-700 rounded-lg shadow-md"
      @mouseleave="() => openOptions = false">
      <p class="mb-1 font-bold text-xs">Map type</p>
      <div>
        <input type="radio" class="mr-1" id="radio-openstreetmap" name="radio-openstreetmap"
          :checked="store.mapStyle === 'openstreetmap'" v-on:change="store.mapStyle = 'openstreetmap'" />
        <label class="text-xs" for="radio-openstreetmap">OpenStreetMap</label>
      </div>
      <div>
        <input type="radio" class="mr-1" id="radio-opentopomap" name="radio-opentopomap"
          :checked="store.mapStyle === 'opentopomap'" v-on:change="store.mapStyle = 'opentopomap'" />
        <label class="text-xs" for="radio-opentopomap">OpenTopoMap</label>
      </div>
      <div>
        <input type="radio" class="mr-1" id="radio-satellite" name="radio-satellite"
          :checked="store.mapStyle === 'satellite'" v-on:change="store.mapStyle = 'satellite'" />
        <label class="text-xs" for="radio-satellite">Satellite</label>
      </div>
    </div>
  </MglCustomControl>
</template>
<script setup lang="ts">
// Documentation: https://indoorequal.github.io/vue-maplibre-gl/api/MglCustomControl.html
import { MglCustomControl } from "@indoorequal/vue-maplibre-gl";
import type { ControlPosition } from "maplibre-gl";
import { ref } from "vue";
import { useStore } from "../../stores/store";

const store = useStore();

export type LayerSelectorProps = {
	position: ControlPosition | undefined;
};

const props = defineProps<LayerSelectorProps>();

const openOptions = ref(false);
</script>
