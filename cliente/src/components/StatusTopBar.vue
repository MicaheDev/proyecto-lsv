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
    <div class="c-stats" v-if="user_data && user_data.user_info">

        <span> Nivel {{ user_data.user_info.stats.current_level }}</span>
        <span>
            Racha {{ user_data.user_info.stats.current_streak }}
        </span>

        <span>
            Puntos {{ user_data.user_info.stats.total_score }}
        </span>

        <span>
            Vidas {{ user_data.user_info.stats.current_hearts }}
        </span>

    </div>
</template>

<style scoped>
.c-stats {
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