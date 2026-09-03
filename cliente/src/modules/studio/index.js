import StudioLayout from "@/core/layouts/StudioLayout.vue";

export const studioRoutes = [
  {
    path: "/",
    component: StudioLayout,
    children: [
        {
        path: "studio",
        name: "studio",
        component: () => import("./views/StudioView.vue"),
      },
    ]
  },

];
