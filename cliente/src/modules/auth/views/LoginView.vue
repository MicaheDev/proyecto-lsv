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
        const response = await axios.post("http://localhost:5000/api/v1/login", payload);
        console.log("Sesion Iniciada:", response.data);
        const {token, user} = response.data
        const user_data = {
            token: token,
            user_info: user
        }
        localStorage.setItem('user_data', JSON.stringify(user_data))
        router.push('/learning');

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

    <div class="c-login-container">
        <form @submit.prevent="handleOnSubmit">

        <h1>Login</h1>
        <br>
        <label for="username">Nombre de usuario</label><br>
        <input type="text" id="username" v-model="form.username" minlength="4" pattern="^\S+$"
            title="No se permiten espacios" required placeholder="pedrito20"><br>
        <br>
        <label for="password">Contraseña</label><br>
        <input type="password" id="password" v-model="form.password" required placeholder="••••"><br>
        <br>

        <button type="submit" :disabled="isLoading">
            {{ isLoading ? 'Accediendo...' : 'Acceder' }}
        </button>
    </form>
    <br>
    <RouterLink to="register">Crear una cuenta</RouterLink>
    </div>
</template>

<style scoped>
.c-login-container{
    width: 100%;
    height: 100svh;

    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;

    padding: 20px;
}

h1 {
    text-align: center;
}

form {
    width: 100%;
}

input {
    width: 100%;
    padding: 10px 8px;
}

button {
    width: 100%;
    padding: 20px;
}
</style>