<template>
  <Listbox as="div" v-model="selected">
    <ListboxLabel class="block text-sm/6 font-medium text-gray-200">{{ props.title }}</ListboxLabel>
    <div class="relative mt-0.5">
      <ListboxButton
        class="grid w-full cursor-default grid-cols-1 rounded-md bg-white py-1.5 pl-3 pr-2 text-left text-gray-900 outline -outline-offset-1 outline-gray-300 focus:outline focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6">
        <span class="col-start-1 row-start-1 truncate pr-6">{{ selected.title }}</span>
        <ChevronUpDownIcon class="col-start-1 row-start-1 size-5 self-center justify-self-end text-gray-500 sm:size-4"
          aria-hidden="true" />
      </ListboxButton>

      <transition leave-active-class="transition ease-in duration-100" leave-from-class="opacity-100"
        leave-to-class="opacity-0">
        <ListboxOptions
          class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black/5 focus:outline-none sm:text-sm">
          <ListboxOption as="template" v-for="option in props.options" :key="option.id" :value="option"
            v-slot="{ active, selected }">
            <li
              :class="[selected ? 'bg-indigo-500 text-white outline-none' : 'text-gray-900', active ? 'bg-indigo-600 text-white outline-none' : 'text-gray-900', 'relative cursor-default select-none py-2 pl-3 pr-9']">
              <span class="block truncate">{{ option.title }}</span>

              <span v-if="props.deleteBtn" class="absolute inset-y-0 right-0 flex items-center pr-4">
                <MinusIcon class="size-5 bg-red-500 text-white rounded-sm cursor-pointer"
                  @click="emit('delete:option', option.id)" aria-hidden="true" />
              </span>
            </li>
          </ListboxOption>
        </ListboxOptions>
      </transition>
    </div>
  </Listbox>
</template>

<script setup lang="ts">
import {
	Listbox,
	ListboxButton,
	ListboxLabel,
	ListboxOption,
	ListboxOptions,
} from "@headlessui/vue";
import { ChevronUpDownIcon, MinusIcon } from "@heroicons/vue/16/solid";
import { computed } from "vue";

export type DropDownProps = {
	title: string;
	options: Array<{ id?: number | string; title: string }>;
	selected?: { id: number; title: string };
	deleteBtn?: boolean;
};

const props = defineProps<DropDownProps>();
const emit = defineEmits(["update:selected", "delete:option"]);

const selected = computed({
	get: () => {
		return props.selected ?? props.options[0];
	},
	set: (value) => {
		emit("update:selected", value);
	},
});
</script>