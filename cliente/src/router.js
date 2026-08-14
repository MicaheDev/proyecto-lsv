import {
  createRouter,
  createWebHistory,
} from "vue-router";

import { authGuard } from "@/core/guards/authGuard";
import { authRoutes } from "@/modules/auth";
import { onboardingRoutes } from "@/modules/onboarding";
import { learningRoutes } from "@/modules/learning";
import { socialRoutes } from "@/modules/social";
import { dictionaryRoutes } from "@/modules/dictionary";

const routes = [
  ...onboardingRoutes,
  ...authRoutes,
  ...learningRoutes,
  ...socialRoutes,
  ...dictionaryRoutes
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// EL GUARDÍAN DE NAVEGACIÓN (beforeEach)
router.beforeEach(authGuard);
export default router;
