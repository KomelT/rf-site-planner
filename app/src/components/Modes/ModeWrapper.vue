<template>
  <div class="pb-5">
    <div class="flex items-center justify-between pt-2 mb-5">
      <div class="flex items-center gap-2 text-lg font-bold cursor-pointer" @click="$emit('backButtonClick')">
        <ArrowLeftIcon class="size-6" />
        {{ props.title }}
      </div>
      <button type="button" class="cursor-pointer -m-2.5 rounded-md p-2.5 text-gray-700"
        @click="store.mobileMenuOpen = false">
        <span class="sr-only">Close menu</span>
        <XMarkIcon class="size-6 text-gray-200" aria-hidden="true" />
      </button>
    </div>
    <slot />
  </div>
</template>
<script setup lang="ts">
import { ArrowLeftIcon, XMarkIcon } from "@heroicons/vue/24/outline";
import { useStore } from "../../stores/store";

const store = useStore();
export type ModeWrapperProps = {
	title: string;
};

const props = defineProps<ModeWrapperProps>();
</script>