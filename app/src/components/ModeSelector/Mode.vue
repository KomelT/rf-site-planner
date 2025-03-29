<template>
  <div class="m-auto group relative cursor-pointer" @click="props.onClick">
    <p class="pb-2">{{ props.title }}</p>
    <img :src="image" />
    <div
      class="absolute z-10 left-0 top-0 w-full h-full hidden group-hover:block bg-stone-900 opacity-95 text-white p-2">
      <p class="text-sm pb-2 font-bold">{{ props.title }}</p>
      <p class="text-sm">{{ props.description }}</p>
    </div>
  </div>
</template>
<script setup lang="ts">
import { ref, watch } from "vue";

export type ModeProps = {
	title: string;
	description: string;
	image: Promise<typeof import("*.jpg") | typeof import("*.png")>;
	onClick: () => void;
};

const props = defineProps<ModeProps>();

const image = ref<string>("");
watch(
	() => props.image,
	(newImage) => {
		newImage.then((img) => {
			image.value = img.default;
		});
	},
	{ immediate: true },
);
</script>