<template>
  <div :class="store.mobileMenuOpen ? 'block' : 'hidden'">
    <div class="inset-y-0 w-96 h-full overflow-y-auto bg-stone-800 px-4 py-5 sm:max-w-sm sm:ring-1 sm:ring-gray-900/10">
      <div class="flex items-center justify-between">
        <a href="/" class="flex items-center -m-1.5 pl-1.5">
          <span class="sr-only">RF Site Planner</span>
          <img class="h-8 mr-2 w-auto" src="/meshnet-logo-light.svg" alt="RF Site Planner Logo" />
          <span class="text-gray-200 text-lg font-bold">RF Site Planner</span>
        </a>
        <button type="button" class="cursor-pointer -m-2.5 rounded-md p-2.5 text-gray-700"
          @click="store.mobileMenuOpen = false">
          <span class="sr-only">Close menu</span>
          <XMarkIcon class="size-6 text-gray-200" aria-hidden="true" />
        </button>
      </div>
      <div class="mt-6 flow-root">
        <div class="-my-6 divide-y divide-gray-500/10">
          <div>
            <ModeSelector />
          </div>
          <div class="py-3">
            <a href="https://github.com/KomelT/rf-site-planner" target="_blank"
              class="flex -mx-3 rounded-lg px-3 py-2.5 text-base/7 font-semibold text-gray-200 hover:bg-stone-900">
              <span class="sr-only">Source code</span>
              Source code
              <GitHubIcon class="ml-2" />
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import { XMarkIcon } from "@heroicons/vue/24/outline";
import GitHubIcon from "../assets/GitHubIcon.vue";
import { useStore } from "../stores/store";
import ModeSelector from "./ModeSelector/ModeSelector.vue";

const store = useStore();
</script>