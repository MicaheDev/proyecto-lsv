import MainLayout from "@/core/layouts/MainLayout.vue";

export const learningRoutes = [
  {
    path: "/learning",
    component: MainLayout,
    children: [
      {
        path: "",
        name: "Learning",
        component: () => import("./views/LearningView.vue"),
      },
    ],
  },
];
