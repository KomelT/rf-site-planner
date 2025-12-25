<template>
  <Listbox as="div" v-model="selected">
    <ListboxLabel v-if="props.title" :class="['block! text-sm/6 font-medium', props.btnOptions?.labelColor ?? 'text-gray-200']">{{ props.title }}</ListboxLabel>
    <div class="relative! mt-0.5">
      <ListboxButton
        class="inline-flex! w-full! min-w-36! cursor-default! items-center! justify-between! gap-2! rounded-md bg-white! py-1.5! pl-3! pr-2! text-left text-gray-900! outline! -outline-offset-1! outline-gray-300! focus:outline! focus:-outline-offset-2! focus:outline-indigo-600! sm:text-sm/6">
        <span class="truncate">{{ selected.title }}</span>
        <ChevronUpDownIcon class="size-5 shrink-0 text-gray-500 sm:size-4" aria-hidden="true" />
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
import { type Ref, computed, ref, watch } from "vue";

export type DropDownProps = {
  title?: string;
  options: Array<{ id?: number | string; title: string }>;
  selected?: { id: number | string; title: string };
  deleteBtn?: boolean;
  btnOptions?: {
    labelColor?: string;
  }
};

const props = defineProps<DropDownProps>();
const emit = defineEmits(["update:selected", "delete:option"]);

const select: Ref<{ id?: string | number | undefined; title: string }> = ref(
  props.options[0],
);

const selected = computed({
  get: () => {
    return props.selected ?? select.value;
  },
  set: (value) => {
    emit("update:selected", value);
    select.value = value;
  },
});

watch(
  () => props.options,
  (options) => {
    if (options.find((opt) => opt.id === selected.value.id)) selected.value = options[0];
  },
);
</script>
