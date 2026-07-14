import {
  createMemoryHistory,
  createRouter,
  createWebHistory,
} from "vue-router";
import HomeView from "./views/HomeView.vue";
import LoginView from "./views/LoginView.vue";
import RegisterView from "./views/RegisterView.vue";
import WelcomeView from "./views/WelcomeView.vue";
import LearnView from "./views/LearnView.vue";
import Scaffold from "./layouts/Scaffold.vue";

const routes = [
  { path: "/", component: HomeView },
  { path: "/welcome", component: WelcomeView },
  { path: "/register", component: RegisterView },
  { path: "/login", component: LoginView },
  {
    path: "/learn",
    name: "learn",
    component: LearnView,
    meta: { layout: Scaffold, requiresAuth: true },
  },
];

const router = createRouter({
  // Note: We're using createMemoryHistory() here for compatibility
  //       with the Playground. In a real application you'd usually
  //       use createWebHistory() or createWebHashHistory() instead,
  //       tying the route to the browser URL. See the documentation
  //       for more information about history modes.
  history: createWebHistory(),
  routes,
});

// =========================================================
// 🛡️ EL GUARDÍAN DE NAVEGACIÓN (beforeEach)
// =========================================================
router.beforeEach((to, from, next) => {
  // 1. Revisamos si el usuario está autenticado (si existe el token)
  const isAuthenticated = !!localStorage.getItem('user_data');
  
  // 2. Revisamos si la ruta a la que intenta ir requiere autenticación
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);

  // CASO 1: Intenta ir a una ruta protegida (como /learn) pero no está logueado
  if (requiresAuth && !isAuthenticated) {
    // Lo rebotamos al Home principal
    return next('/login'); 
  }

  // CASO 2: Si ya está logueado e intenta ir al Login, Registro o Home, lo mandamos directo al módulo de aprendizaje
  if (isAuthenticated && (to.path === '/login' || to.path === '/register' || to.path === '/')) {
    return next('/learn');
  }

  // CASO 3: Si no cumple ninguna de las anteriores, lo dejamos pasar libremente
  next();
});

export default router;
