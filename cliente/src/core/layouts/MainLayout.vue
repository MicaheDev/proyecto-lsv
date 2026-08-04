<script setup>

import BottomNav from "../components/BottomNav.vue";
import StatusTopBar from "../components/StatusTopBar.vue";


</script>

<template>
  <div class="c-container">
    <StatusTopBar />
    <main class="c-content">
      <RouterView />
    </main>
    <BottomNav />
  </div>
</template>

<style scoped>
.c-container {
  width: 100%;
  height: 100svh;

  display: flex;
  flex-direction: column;

  overflow: hidden;
}

.c-content {
  width: 100%;
  height: 100%;
  overflow-y: auto;
}
</style>
