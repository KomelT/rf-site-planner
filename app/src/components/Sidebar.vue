<template>
  <div :class="store.mobileMenuOpen ? 'block' : 'hidden'">
    <div
      class="inset-y-0 sm:w-96 h-[calc(100vh-64px)] overflow-y-auto bg-stone-800 px-4 pb-5 w-screen sm:ring-1 sm:ring-gray-900/10">
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
import GitHubIcon from "../assets/GitHubIcon.vue";
import { useStore } from "../stores/store";
import ModeSelector from "./ModeSelector/ModeSelector.vue";

const store = useStore();

store.loadFromLocalStorage();
store.watchForChangesAndCommit();
store.coverSimModeData.legend.show = false;
</script>