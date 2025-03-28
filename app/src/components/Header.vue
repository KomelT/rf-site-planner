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
      <div v-if="!mobileMenuOpen" class="lg:flex lg:flex-1 lg:justify-end">
        <a href="https://github.com/KomelT/rf-site-planner" target="_blank"
          class="hidden lg:block text-xll font-semibold text-gray-900">
          <GitHubIcon />
        </a>
        <button type="button"
          class="cursor-pointer ml-3 -m-2.5 inline-flex items-center justify-center rounded-md p-2.5 text-gray-700"
          @click="mobileMenuOpen = true">
          <span class="sr-only">Open main menu</span>
          <Bars3Icon class="size-6 text-gray-200" aria-hidden="true" />
        </button>
      </div>
    </nav>
    <div v-if="mobileMenuOpen">
      <div
        class="fixed inset-y-0 right-0 z-10 w-full overflow-y-auto bg-stone-800 px-4 py-5 sm:max-w-sm sm:ring-1 sm:ring-gray-900/10">
        <div class="flex items-center justify-between">
          <a href="/" class="flex items-center -m-1.5 pl-1.5">
            <span class="sr-only">RF Site Planner</span>
            <img class="h-8 mr-2 w-auto" src="/meshnet-logo-light.svg" alt="RF Site Planner Logo" />
            <span class="text-gray-200 text-lg font-bold">RF Site Planner</span>
          </a>
          <button type="button" class="cursor-pointer -m-2.5 rounded-md p-2.5 text-gray-700"
            @click="mobileMenuOpen = false">
            <span class="sr-only">Close menu</span>
            <XMarkIcon class="size-6 text-gray-200" aria-hidden="true" />
          </button>
        </div>
        <div class="mt-6 flow-root">
          <div class="-my-6 divide-y divide-gray-500/10">
            <div class="space-y-2 py-2">
              <a v-for="item in navigation" :key="item.name" :href="item.href"
                class="-mx-3 block rounded-lg px-3 py-2 text-base/7 font-semibold text-gray-900 hover:bg-gray-50">{{
                  item.name }}</a>
            </div>
            <div>
              <slot />
            </div>
            <div class="py-3">
              <a href="https://github.com/KomelT/rf-site-planner" target="_blank"
                class="flex -mx-3 block rounded-lg px-3 py-2.5 text-base/7 font-semibold text-gray-200 hover:bg-stone-900">
                <span class="sr-only">Source code</span>
                Source code
                <GitHubIcon class="ml-2" />
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref } from 'vue'
import { Dialog, DialogPanel } from '@headlessui/vue'
import { Bars3Icon, XMarkIcon } from '@heroicons/vue/24/outline'
import GitHubIcon from '../assets/GitHubIcon.vue'

// { name: 'Product', href: '#' }
const navigation = []

// set default value as false if screen size is less than 1024px
const mobileMenuOpen = ref(true)
if (window.innerWidth < 1024) {
  mobileMenuOpen.value = false
} else {
  mobileMenuOpen.value = true
}
</script>