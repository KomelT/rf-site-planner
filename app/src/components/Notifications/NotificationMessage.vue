<template>
  <transition enter-active-class="transform ease-out duration-300 transition"
    enter-from-class="translate-y-2 opacity-0 sm:translate-y-0 sm:translate-x-2"
    enter-to-class="translate-y-0 opacity-100 sm:translate-x-0" leave-active-class="transition ease-in duration-100"
    leave-from-class="opacity-100" leave-to-class="opacity-0">
    <div
      class="pointer-events-auto w-full max-w-sm overflow-hidden rounded-lg bg-white shadow-lg ring-1 ring-black ring-opacity-5">
      <div class="p-4">
        <div class="flex items-start">
          <div class="flex-shrink-0">
            <InformationCircleIcon v-if="props.type === 'info'" class="h-6 w-6 text-blue-400" aria-hidden="true" />
            <CheckCircleIcon v-if="props.type === 'success'" class="h-6 w-6 text-green-400" aria-hidden="true" />
            <ExclamationCircleIcon v-if="props.type === 'warning'" class="h-6 w-6 text-yellow-400" aria-hidden="true" />
            <XCircleIcon v-if="props.type === 'error'" class="h-6 w-6 text-red-400" aria-hidden="true" />
          </div>
          <div class="ml-3 w-0 flex-1 pt-0.5">
            <p class="text-sm font-medium text-gray-900">{{ props.title }}</p>
            <p class="mt-1 text-sm text-gray-500">{{ props.message }}</p>
          </div>
          <div class="ml-4 flex flex-shrink-0">
            <button type="button" @click="() => emit('self:close')"
              class="inline-flex rounded-md bg-white text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2">
              <span class="sr-only">Zapri</span>
              <XMarkIcon class="h-5 w-5" aria-hidden="true" />
            </button>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup lang="ts">
import { XMarkIcon } from "@heroicons/vue/16/solid";
import {
	CheckCircleIcon,
	ExclamationCircleIcon,
	InformationCircleIcon,
	XCircleIcon,
} from "@heroicons/vue/24/outline";
import type { Notification } from "../../stores/notification";

export type NotificationMessageProps = Omit<Notification, "id" | "hideAfter">;

const props = defineProps<NotificationMessageProps>();

const emit = defineEmits(["self:close"]);
</script>