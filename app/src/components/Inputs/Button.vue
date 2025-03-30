<template>
  <button type="button" @click="props.onClick" :class="props.class"
    class="rounded bg-orange-500 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-orange-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-orange-500">{{
      props.text }}</button>
</template>
<script setup lang="ts">
type ButtonProps = {
	text: string;
	onClick: () => void;
	class?: string;
};

const props = defineProps<ButtonProps>();
</script>