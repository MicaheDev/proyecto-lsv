<script setup>
import { onMounted, ref } from 'vue';

// 1. Lo inicializamos estrictamente en null
const user_data = ref(null);

onMounted(() => {
    const rawData = localStorage.getItem('user_data');
    if (rawData) {
        try {
            // Si existen datos, procesamos el JSON
            user_data.value = JSON.parse(rawData);
        } catch (e) {
            // Por seguridad, si el JSON está corrupto, lo dejamos en null
            user_data.value = null;
        }
    }
});



</script>

<template>
    <div class="w-full h-svh flex flex-col overflow-hidden">
        <header class="w-full h-20 flex shrink-0 justify-between items-center px-6 border-b"
            v-if="user_data && user_data.user_info">
            <span> {{ user_data.user_info.username }}</span>

        </header>
        <main class="w-full h-full overflow-y-auto">
            <RouterView />
        </main>

    </div>
</template>
