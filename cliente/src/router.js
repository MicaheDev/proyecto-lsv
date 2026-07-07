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

const routes = [
  { path: "/", component: HomeView },
  { path: "/welcome", component: WelcomeView },
  { path: "/register", component: RegisterView },
  { path: "/login", component: LoginView },
  { path: "/learn", component: LearnView },
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

export default router;
