<template>
  <div class="flex flex-row items-center justify-between mt-3 cursor-pointer"
    @click="emit('update:showSection', !props.showSection)">
    <span class="flex flex-row items-center">
      <p class="mt-3 mb-1 cursor-pointer">{{ props.title }}</p>
      <MapLibreMarker v-if="props.markerColor" :height="30" :color="props.markerColor" />
    </span>
    <ArrowDownIcon v-if="props.showSection" class="w-4 h-4 text-stone-400" />
    <ArrowRightIcon v-else class="w-4 h-4 text-stone-400" />
  </div>
  <div :class="['p-3 bg-stone-700 rounded-xl', props.showSection ? 'block' : 'hidden']">
    <slot />
  </div>
</template>
<script setup lang="ts">
import { ArrowDownIcon, ArrowRightIcon } from "@heroicons/vue/24/outline";
import MapLibreMarker from "../../assets/MapLibreMarker.vue";

type ModeDataAccordianProps = {
	title: string;
	showSection: boolean;
	markerColor?: string;
};

const props = defineProps<ModeDataAccordianProps>();
const emit = defineEmits(["update:showSection"]);
</script>