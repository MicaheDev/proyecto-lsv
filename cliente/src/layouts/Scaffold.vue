<script setup>
import { computed } from 'vue';
import BottomNav from '../components/BottomNav.vue';
import { useRoute } from 'vue-router';

const route = useRoute();

const activeTopBar = computed(() => route.meta.topBar);
const shouldShowBottomNav = computed(() => route.meta.showBottomNav ?? false);
</script>

<template>
    <div class="c-container">
        <component :is="activeTopBar" v-if="activeTopBar" />
        <main class="c-content">
            <slot />
        </main>
        <BottomNav v-if="shouldShowBottomNav" />
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