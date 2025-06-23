<template>
  <button type="button" @click="props.onClick" :disabled="props.disabled"
    :class="['flex gap-2 rounded bg-orange-500 px-3 py-2 text-sm font-semibold text-white shadow-sm cursor-pointer hover:bg-orange-400 focus-visible:outline focus-visible:outline-offset-2 focus-visible:outline-orange-500 disabled:cursor-not-allowed', props.class]">{{
      props.text }}
    <ArrowPathIcon v-if="props.loading" class="size-6 animate-spin" />
  </button>
</template>
<script setup lang="ts">
import { ArrowPathIcon } from "@heroicons/vue/24/outline";

type ButtonProps = {
	text: string;
	onClick: () => void;
	class?: string | string[];
	loading?: boolean;
	disabled?: boolean;
};

const props = defineProps<ButtonProps>();
</script>