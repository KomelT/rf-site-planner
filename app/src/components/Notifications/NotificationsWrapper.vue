<template>
  <div aria-live="assertive"
    class="pointer-events-none fixed inset-0 flex items-end px-4 py-6 z-40 sm:items-start sm:p-6">
    <div class="flex w-full flex-col items-center space-y-4 sm:items-end">
      <KNotificationMessage v-for="not in notificationStore.notifications" :type="not.type" :title="not.title"
        :message="not.message" :key="not.id" v-on:self:close="() => notificationStore.closeNotification(not.id)" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { useNotificationStore } from "../../stores/notification";
import KNotificationMessage from "./NotificationMessage.vue";

const notificationStore = useNotificationStore();
</script>