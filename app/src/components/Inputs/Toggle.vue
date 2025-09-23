<template>
  <div>
    <label for="text" class="block text-sm/6 font-medium text-gray-200">{{ props.title }}</label>
    <div
      class="mt-0.5 group relative inline-flex w-11 shrink-0 rounded-full bg-gray-200 p-0.5 outline-offset-2 bg-gray-500 ring-1 ring-inset ring-gray-900/5 transition-colors duration-200 ease-in-out has-[:checked]:bg-orange-500 has-[:focus-visible]:outline has-[:focus-visible]:outline-2">
      <span
        class="size-5 rounded-full bg-white shadow-sm ring-1 ring-gray-900/5 transition-transform duration-200 ease-in-out group-has-[:checked]:translate-x-5" />
      <input type="checkbox" class="absolute inset-0 appearance-none focus:outline-none" aria-label="Use setting"
        name="setting" v-model="value" />
    </div>
  </div>
</template>
<script setup lang="ts">
import { computed } from "vue";

type ButtonProps = {
  title: string;
  value: boolean;
};

const props = defineProps<ButtonProps>();
const emit = defineEmits(["update:value"]);

const value = computed({
	get: () => props.value,
	set: (value: string) => emit("update:value", value),
});
</script>