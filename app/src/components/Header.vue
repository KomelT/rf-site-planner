<template>
  <header class="bg-stone-800">
    <nav class="mx-auto flex max-w-7xl items-center justify-between p-4 lg:px-4" aria-label="Global">
      <div class="">
        <a href="/" class="flex items-center lg:flex-1 -m-1.5 p-1.5" style="text-decoration: none;">
          <span class="sr-only">RF Site Planner</span>
          <img class="h-8 w-auto mr-2" src="/meshnet-logo-light.svg" alt="RF Site Planner Logo" />
          <span class="text-gray-200 text-lg font-bold">RF Site Planner</span>
        </a>
      </div>
      <div class="lg:flex lg:gap-x-12">
        <a v-for="item in navigation" :key="item.name" :href="item.href"
          class="text-sm/6 font-semibold text-gray-900">{{ item.name }}</a>
      </div>
      <div v-if="!store.mobileMenuOpen" class="lg:flex lg:flex-1 lg:justify-end">
        <a href="https://github.com/KomelT/rf-site-planner" target="_blank"
          class="hidden lg:block text-xll font-semibold text-gray-900">
          <GitHubIcon />
        </a>
        <button type="button"
          class="cursor-pointer ml-3 -m-2.5 inline-flex items-center justify-center rounded-md p-2.5 text-gray-700"
          @click="store.mobileMenuOpen = true">
          <span class="sr-only">Open main menu</span>
          <Bars3Icon class="size-6 text-gray-200" aria-hidden="true" />
        </button>
      </div>
    </nav>
  </header>
</template>

<script setup>
import { Bars3Icon } from "@heroicons/vue/24/outline";
import GitHubIcon from "../assets/GitHubIcon.vue";
import { useStore } from "../stores/store";

const store = useStore();

// { name: 'Product', href: '#' }
const navigation = [];

// set default value as false if screen size is less than 1024px
if (window.innerWidth < 1024) {
  store.mobileMenuOpen = false;
} else {
  store.mobileMenuOpen = true;
}
</script>