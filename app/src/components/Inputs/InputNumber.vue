<template>
  <div>
    <label for="number" class="block text-sm/6 font-medium text-gray-200">{{ props.title }}</label>
    <div class="mt-0.5">
      <input type="number" v-model="value" name="number" id="number" :max="props.max" :min="props.min"
        :step="props.step"
        class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"
        :disabled="props.disabled" />
    </div>
  </div>
</template>
<script setup lang="ts">
import { computed } from "vue";

export type NumberProps = {
  title: string;
  value: number;
  max?: number;
  min?: number;
  step?: number;
  disabled?: boolean;
};

const props = defineProps<NumberProps>();
const emit = defineEmits(["update:value"]);

const value = computed({
  get: () => props.value,
  set: (value: number) => emit("update:value", value),
});
</script>