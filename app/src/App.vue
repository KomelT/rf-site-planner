<template>
  <div>
    <Header />
    <div class="flex">
      <CMap />
      <Sidebar />
    </div>
    <NotificationsWrapper />
  </div>
</template>

<script setup lang="ts">
import CMap from "./components/CMap.vue";
import Header from "./components/Header.vue";
import NotificationsWrapper from "./components/Notifications/NotificationsWrapper.vue";
import Sidebar from "./components/Sidebar.vue";
</script>
