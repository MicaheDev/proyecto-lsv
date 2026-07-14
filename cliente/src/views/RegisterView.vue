<script setup>
import { reactive, onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter();
const isLoading = ref(false); // Un simple booleano para el botón, sin composables raros

const form = reactive({
    fullName: "",
    username: "",
    password: "",
    confirmPassword: ""
});

let onboardingPreferences = ref({});

onMounted(() => {
    const rawData = localStorage.getItem('temp_preferences_data');
    onboardingPreferences.value = rawData ? JSON.parse(rawData) : {};
});

async function handleOnSubmit() {
    // 1. La única validación manual en JS: que las contraseñas coincidan
    if (form.password !== form.confirmPassword) {
        alert("❌ Las contraseñas no coinciden.");
        return;
    }

    isLoading.value = true;

    const payload = {
        full_name: form.fullName,
        username: form.username,
        password: form.password,
        preferences: {
            role_id: onboardingPreferences.value.relationship || "community",
            level_preference: onboardingPreferences.value.lsvLevel || "None", // 'None' con N mayúscula igual que tu CHECK
            daily_goal: parseInt(onboardingPreferences.value.dailyGoal) || 10, // Aseguramos que viaje como número
            audio_mode: onboardingPreferences.value.audioMode || "full_audio",
            is_simplified: onboardingPreferences.value.uiAccessibility ? onboardingPreferences.value.uiAccessibility === 'simplified' : false
        }
    };

    try {
        // 2. Fetch directo con Axios
        const response = await axios.post("http://127.0.0.1:5000/api/v1/register", payload);

        console.log("Registro exitoso:", response.data);
        const { token, user } = response.data
        const user_data = {
            token: token,
            user_info: user
        }
        localStorage.setItem('user_data', JSON.stringify(user_data))
        localStorage.removeItem('temp_preferences_data');
        router.push('/learn');

    } catch (error) {
        console.error("Error al registrar:", error);
        // Si Flask dice que el usuario ya existe, te lo muestra en un alert nativo aquí
        const msg = error.response?.data?.message || "No se pudo conectar con el servidor.";
        alert(`⚠️ Error: ${msg}`);
    } finally {
        isLoading.value = false;
    }
}
</script>

<template>
   <div class="c-register-container">
     <form @submit.prevent="handleOnSubmit">
        <h1>Register</h1>
        <br>

        <label for="full_name">Nombre completo</label><br>
        <input type="text" id="full_name" v-model="form.fullName" minlength="3" required placeholder="Pedro Pérez"><br>
        <br>

        <label for="username">Nombre de usuario</label><br>
        <input type="text" id="username" v-model="form.username" minlength="4" pattern="^\S+$"
            title="No se permiten espacios" required placeholder="pedrito20"><br>
        <br>

        <label for="password">Contraseña</label><br>
        <input type="password" id="password" v-model="form.password" minlength="4" required placeholder="••••"><br>
        <br>

        <label for="confirm-password">Confirmar Contraseña</label><br>
        <input type="password" id="confirm-password" v-model="form.confirmPassword" required placeholder="••••"><br>
        <br>

        <button type="submit" :disabled="isLoading">
            {{ isLoading ? 'Registrando...' : 'Registrarse e Ingresar' }}
        </button>
    </form>

    <br>
    <RouterLink to="login">Ya tengo una cuenta</RouterLink>

   </div>
</template>

<style scoped>
.c-register-container {
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