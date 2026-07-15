<script setup>

const menu = [
  {
    path: "/manage",
    name: "Inicio",
  },
  {
    path: "/studio",
    name: "Estudio",
  },
]

</script>


<template>

  <nav class="c-nav">

    <RouterLink v-for="el in menu" :key="el.name" :to="el.path">

      <span>{{ el.name }}</span>

    </RouterLink>

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

  border-top: 1px solid black;
}
</style>