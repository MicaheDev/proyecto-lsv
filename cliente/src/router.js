import { createMemoryHistory, createRouter } from 'vue-router'
import HomeView from './views/Home/HomeView.vue'


const routes = [
  { path: '/', component: HomeView },
]

const router = createRouter({
  // Note: We're using createMemoryHistory() here for compatibility
  //       with the Playground. In a real application you'd usually
  //       use createWebHistory() or createWebHashHistory() instead,
  //       tying the route to the browser URL. See the documentation
  //       for more information about history modes.
  history: createMemoryHistory(),
  routes,
})

export default router