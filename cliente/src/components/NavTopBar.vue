<script setup>
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
const router = useRouter();

function goBack() {
  if (window.history.length > 1) {
    router.back();
  } else {
    router.push('/learn'); // Ruta segura de escape
  }
}

</script>

<template>
  <nav class="c-nav">
    <button class="back-btn" @click="goBack" aria-label="Volver atrás">
      Volver
    </button>
  </nav>
</template>

<style scoped>
.c-nav {
  flex-shrink: 0;

  width: 100%;
  height: 80px;

  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-inline: 20px;

  border-bottom: 1px solid black;
}
</style>