<script setup>
import { computed } from 'vue';
import BottomNav from '../components/BottomNav.vue';
import { useRoute } from 'vue-router';

const route = useRoute();

const activeTopBar = computed(() => route.meta.topBar);
const activeBottomBar = computed(() => route.meta.bottomBar);
</script>

<template>
    <div class="c-container">
        <component :is="activeTopBar" v-if="activeTopBar" />
        <main class="c-content">
            <RouterView />
        </main>
        <component :is="activeBottomBar" v-if="activeBottomBar" />
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