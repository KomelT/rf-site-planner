<template>
  <div>
    <div class="flex items-center gap-2 text-lg font-bold pt-2 mb-5 cursor-pointer" @click="$emit('backButtonClick')">
      <ArrowLeftIcon class="size-6" />
      {{ props.title }}
    </div>
    <slot />
  </div>
</template>
<script setup lang="ts">
import { ArrowLeftIcon } from "@heroicons/vue/24/outline";

export type ModeWrapperProps = {
	title: string;
};

const props = defineProps<ModeWrapperProps>();
</script>