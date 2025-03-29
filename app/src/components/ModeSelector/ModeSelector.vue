<template>
  <div v-if="showSelector">
    <p class="text-lg font-bold py-2">Select mode:</p>
    <div class="grid grid-cols-2 gap-2">
      <Mode v-for="(mode, index) in modes" :key="index" :title="mode.title" :description="mode.description"
        :image="mode.image" :onClick="mode.onClick" />
    </div>
  </div>
</template>
<script setup lang="ts">
import { computed, ref } from "vue";
import Mode from "./Mode.vue";

const showCoverageSim = ref(false);

const showSelector = computed(() => {
  return !(showCoverageSim.value);
});

const modes = [
  {
    title: "Coverage simulator:",
    description: "Simulate coverage of a mesh network",
    image: import("../../assets/coverage-simulator.jpg"),
    onClick: () => { showCoverageSim.value = true },
  },
];
</script>