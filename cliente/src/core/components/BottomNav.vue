<script setup>

const menu = [
  {
    path: "/learning",
    name: "Inicio",
  },

  {
    path: "/dictionary",
    name: "Diccionario",
  },

  {
    path: "/rank",
    name: "Rank",
  },
  {
    path: "/profile",
    name: "Perfil",
  }
]

</script>


<template>
  <nav class="w-full h-20 flex shrink-0 justify-between items-center px-6 border-t">
    <RouterLink v-for="el in menu" :key="el.name" :to="el.path">
      <span>{{ el.name }}</span>
    </RouterLink>
  </nav>
</template>
