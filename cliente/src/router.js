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
import ProfileView from "./views/ProfileView.vue";
import StatusTopBar from "./components/StatusTopBar.vue";
import SignsView from "./views/SignsView.vue";
import RankingView from "./views/RankingView.vue";
import BottomNav from "./components/BottomNav.vue";
import AdminToBar from "./components/AdminToBar.vue";
import AdminBottomNav from "./components/AdminBottomNav.vue";
import DashboardView from "./views/manage/DashboardView.vue";
import axios from "axios";

const routes = [
  { path: "/", component: HomeView },
  { path: "/welcome", component: WelcomeView },
  { path: "/register", component: RegisterView },
  { path: "/login", component: LoginView },
  {
    path: "/",
    // El Scaffold actúa como el contenedor padre de este grupo de rutas
    component: Scaffold,
    meta: {
      requiresAuth: true,
      topBar: StatusTopBar,
      bottomBar: BottomNav,
    },
    children: [
      {
        path: "learn",
        name: "Learn",
        component: LearnView,
      },
      {
        path: "signs",
        name: "signs",
        component: SignsView,
      },
      {
        path: "ranking",
        name: "ranking",
        component: RankingView,
      },
      {
        path: "profile",
        name: "profile",
        component: ProfileView,
        meta: {
          topBar: null,
        },
      },
    ],
  },
  {
    path: "/manage",
    name: "Manage",
    component: Scaffold,
    meta: {
      requiresAuth: true,
      requiresAdmin: true,
      topBar: AdminToBar,
      bottomBar: AdminBottomNav,
    },
    children: [
      {
        path: "/",
        name: "Dashboard",
        component: DashboardView,
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// =========================================================
// 🛡️ EL GUARDÍAN DE NAVEGACIÓN (beforeEach)
// =========================================================
router.beforeEach(async (to, from, next) => {
  const userDataRaw = localStorage.getItem("user_data");
  const isAuthenticated = !!userDataRaw;

  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth);
  const requiresAdmin = to.matched.some((record) => record.meta.requiresAdmin);

  // 1. Si la ruta requiere autenticación y no está logueado, al login.
  if (requiresAuth && !isAuthenticated) {
    return next("/login");
  }

  // 2. Si ya está logueado e intenta ir a Login/Register/Home, redirigir según su rol guardado localmente
  if (isAuthenticated && (to.path === "/login" || to.path === "/register" || to.path === "/")) {
    try {
      const parsedData = JSON.parse(userDataRaw);
      // Asumiendo que al hacer login guardas el rol como 'ADMIN' o 'USER'
      if (parsedData.user_info?.role === "ADMIN") {
        return next("/manage");
      }
    } catch (e) {
      console.error("Error leyendo user_data local", e);
    }
    return next("/learn");
  }

  // 3. Proteger la zona de administración consultando al servidor Flask en tiempo real
  if (requiresAdmin) {
    try {
      const parsedData = JSON.parse(userDataRaw);
      const token = parsedData?.token;

      // Hacemos un GET e inyectamos el Bearer Token para pasar el @jwt_required()
      const response = await axios.get("http://127.0.0.1:5000/api/v1/verify", {
        headers: { Authorization: `Bearer ${token}` }
      });

      const { user } = response.data;

      // Si el rol no es 1 (ADMIN), lo rebotamos al ecosistema de estudiante
      if (user.role_id !== 1) {
        alert("⚠️ Acceso denegado: No tienes permisos de administrador.");
        return next("/learn");
      }
    } catch (error) {
      console.error("Error en la verificación de administrador:", error);
      return next("/login"); // Si el token expiró o falló, directo al login
    }
  }

  next();
});
export default router;
