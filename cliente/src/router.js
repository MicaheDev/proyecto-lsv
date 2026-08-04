import {
  createRouter,
  createWebHistory,
} from "vue-router";

import { authGuard } from "@/core/guards/authGuard";
import { authRoutes } from "@/modules/auth";
import { onboardingRoutes } from "./modules/onboarding";
import { learningRoutes } from "./modules/learning";
const routes = [
  ...onboardingRoutes,
  ...authRoutes,
  ...learningRoutes
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// EL GUARDÍAN DE NAVEGACIÓN (beforeEach)
router.beforeEach(authGuard);
export default router;
