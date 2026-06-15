<template>
  <div class="w-full h-svh flex flex-col overflow-hidden overflow-x-auto font-quicksand">
    <!-- Contenedor del scroll con su respectivo Ref y evento de scroll en Vue -->
    <div
      ref="scrollRef"
      @scroll="handleScroll"
      class="w-full h-full flex overflow-x-auto snap-x snap-mandatory scroll-smooth"
      style="scrollbar-width: none;"
    >
      <!-- Bucle for en Vue usando v-for -->
      <div
        v-for="slide in slides"
        :key="slide.id"
        class="w-screen snap-center gap-8 shrink-0 h-full flex flex-col justify-center items-center p-8"
      >
        <h1 class="text-center text-4xl font-black">{{ slide.title }}</h1>
        
        <!-- En Vue combinamos clases fijas y dinámicas pasando un array a :class sin usar clsx -->
        <img
          :class="['rounded-4xl', slide.className]"
          :src="slide.imgSrc"
          alt="Ilustración de la lección"
        />
      </div>
    </div>

    <!-- Indicadores de paginación y botón inferior -->
    <div class="w-full flex flex-col gap-4 justify-center items-center p-8">
      <!-- Indicadores (Puntos flotantes) -->
      <div class="flex gap-2">
        <div
          v-for="(_, index) in slides"
          :key="index"
          :class="[
            'h-2 rounded-full transition-all border duration-300',
            slideActual === index ? 'w-8 bg-amber-300' : 'w-2 bg-gray-300'
          ]"
        />
      </div>

      <!-- Botón de acción principal -->
      <button
        @click="manejarSiguiente"
        class="w-full h-15 border font-black text-xl flex justify-center items-center bg-amber-300 rounded-2xl"
      >
        {{ slideActual === slides.length - 1 ? "Empezar" : "Siguiente" }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

// Definición de las diapositivas (Slides)
const slides = [
  {
    id: "1",
    title: "¡Hola! Vamos a aprender señas juntos",
    imgSrc: "img/1.jpg",
    className: "w-full h-60 object-cover"
  },
  {
    id: "2",
    title: "Mira el video y repite el movimiento",
    imgSrc: "img/2.gif",
    className: "w-40 h-min object-cover"
  },
  {
    id: "3",
    title: "Usa tu cámara para que te ayudemos",
    imgSrc: "img/3.jpg",
    className: "w-full h-60 object-cover"
  }
]

// Estados reactivos (Equivalentes a useState y useRef)
const slideActual = ref(0)
const scrollRef = ref(null)

// Enrutador de Vue Router (Equivalente a useNavigate)
const router = useRouter()

// Detectar en qué diapositiva estamos al hacer scroll horizontal
const handleScroll = () => {
  if (scrollRef.value) {
    const index = Math.round(
      scrollRef.value.scrollLeft / window.innerWidth
    )
    slideActual.value = index
  }
}

// Lógica del botón "Siguiente" o "Empezar"
const manejarSiguiente = () => {
  if (slideActual.value < slides.length - 1) {
    // Hacemos scroll programático usando el ref (.value)
    scrollRef.value?.scrollTo({
      left: window.innerWidth * (slideActual.value + 1)
    })
  } else {
    console.log("Redireccionando al área de aprendizaje...")
    // Navegación hacia la ruta "/aprender" usando Vue Router
    router.push('/aprender')
  }
}
</script>