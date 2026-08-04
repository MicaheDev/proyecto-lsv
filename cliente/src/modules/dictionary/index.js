import MainLayout from "@/core/layouts/MainLayout.vue";

export const dictionaryRoutes = [
  {
    path: "/",
    component: MainLayout,
    children: [
      {
        path: "dictionary",
        name: "Dictionary",
        component: () => import("./views/DictionaryView.vue"),
      },
  
    ],
  },
];
