<script setup>
import BottomNav from "../components/BottomNav.vue";
import StatusTopBar from "../components/StatusTopBar.vue";
</script>

<template>
  <div class="w-full h-svh flex flex-col overflow-hidden">
    <StatusTopBar />
    <main class="w-full h-full overflow-y-auto">
      <RouterView />
    </main>
    <BottomNav />
  </div>
</template>
