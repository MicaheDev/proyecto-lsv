import MainLayout from "@/core/layouts/MainLayout.vue";

export const socialRoutes = [
  {
    path: "/",
    component: MainLayout,
    children: [
      {
        path: "rank",
        name: "Rank",
        component: () => import("./views/RankView.vue"),
      },
       {
        path: "profile",
        name: "Profile",
        component: () => import("./views/ProfileView.vue"),
      },
    ],
  },
];
