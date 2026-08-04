export const authRoutes = [
  {
    path: "/",
    component: () => import("@/core/layouts/AuthLayout.vue"),
    children: [
      {
        path: "login",
        name: "Login",
        component: () => import("./views/LoginView.vue"),
      },
      {
        path: "register",
        name: "Register",
        component: () => import("./views/RegisterView.vue"),
      },
    ],
  },
];
