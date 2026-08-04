export const onboardingRoutes = [
  {
    path: "/",
    name: "Home",
    component: () => import("./views/HomeView.vue"),
  },
  {
    path: "/welcome",
    name: "Welcome",
    component: () => import("./views/WelcomeView.vue"),
  },
];
