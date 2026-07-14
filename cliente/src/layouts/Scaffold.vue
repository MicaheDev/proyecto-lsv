<script setup>
import BottomNav from '../components/BottomNav.vue';
import TopBar from '../components/TopBar.vue';
</script>

<template>
    <div class="c-container">
        <TopBar />
        <main class="c-content">
            <slot />
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

    padding: 20px;

    overflow-y: auto;
}
</style>