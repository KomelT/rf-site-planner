<template>
  <div>
    <label for="text" class="block text-sm/6 font-medium text-gray-200">{{ props.title }}</label>
    <div class="mt-0.5">
      <input type="text" v-model="value" name="text" id="text"
        class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6" />
    </div>
  </div>
</template>
<script setup lang="ts">
import { computed } from "vue";

export type TextProps = {
	title: string;
	value: string;
};

const props = defineProps<TextProps>();
const emit = defineEmits(["update:value"]);

const value = computed({
	get: () => props.value,
	set: (value: string) => emit("update:value", value),
});
</script>