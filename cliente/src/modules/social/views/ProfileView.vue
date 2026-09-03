<script setup>
import { onMounted, ref } from 'vue';
import { useRouter, RouterLink } from 'vue-router';
const router = useRouter();

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
    // Si no hay rawData, user_data se queda siendo null automáticamente
});


function logout() {
    localStorage.removeItem("user_data")
    router.push("/")
}

</script>
<template>
    <div class="p-6 flex flex-col" v-if="user_data && user_data.user_info">

        <span>{{ user_data.user_info.username }}</span>
        <span>{{ user_data.user_info.role }}</span>
        <span>{{ user_data.user_info.full_name }}</span>
        <span>{{ user_data.user_info.stats.current_level }}</span>
        <br>
        <div class="flex flex-col" v-if="user_data.user_info.role == 'ADMIN'">
        <RouterLink to="/studio">Studio</Routerlink>
        </div>
        <br>
        <button class="w-min text-nowrap" v-on:click="logout">Cerrar Sesión</button>
    </div>
</template>

