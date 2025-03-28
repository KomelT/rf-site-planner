<template>
  <div>
    <Header />
    <CMap />
  </div>
</template>

<script setup lang="ts">
import Header from "./components/Header.vue";
import CMap from "./components/CMap.vue"

import { useStore } from "./stores/store.ts";
const store = useStore();
const buttonText = () => {
  if ("running" === store.simulationState) {
    return "Running";
  }
  if ("failed" === store.simulationState) {
    return "Failed";
  }
  return "Run Simulation";
};
</script>
