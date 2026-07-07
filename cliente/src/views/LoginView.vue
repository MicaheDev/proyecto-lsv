<script setup>
import { reactive, onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter();
const isLoading = ref(false); // Un simple booleano para el botón, sin composables raros

const form = reactive({
    username: "",
    password: "",
});

async function handleOnSubmit() {
    isLoading.value = true;

    const payload = {
        username: form.username,
        password: form.password,
    }

    try {
        const response = await axios.post("localhost:5000/api/v1/login", payload);
        console.log("Registro exitoso:", response.data);
        router.push('/learn');

    } catch (error) {
        console.error("Error al registrar:", error);
        // Si Flask dice que el usuario ya existe, te lo muestra en un alert nativo aquí
        const msg = error.response?.data?.message || "No se pudo conectar con el servidor.";
        alert(`⚠️ Error: ${msg}`)
    } finally {
        isLoading.value = false;
    }
}

</script>

<template>

    <form @submit.prevent="handleOnSubmit">

        <h1>Login</h1>
        <br>
        <label for="username">Nombre de usuario</label><br>
        <input type="text" id="username" v-model="form.username" minlength="4" pattern="^\S+$"
            title="No se permiten espacios" required placeholder="pedrito20"><br>
        <br>
        <br>
        <label for="password">Contraseña</label><br>
        <input type="password" id="password" v-model="form.password" minlength="4" required placeholder="••••"><br>
        <br>

        <button type="submit" :disabled="isLoading">
            Ingresar</button>
    </form>
    <br>
    <RouterLink to="register">Crear una cuenta</RouterLink>
</template>