import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import { createBrowserRouter } from "react-router";
import { RouterProvider } from "react-router/dom";

// 1. Imports de tus componentes
import Home from "./views/Home";

// 2. Registro del Service Worker (Importación Virtual)
import { registerSW } from "virtual:pwa-register";
import Layout from "./layouts/Layout";
import Learn from "./views/Learn";

// 3. Ejecución inmediata del registro
const updateSW = registerSW({
  onOfflineReady() {
    console.log("App lista para trabajar offline");
  },
  onNeedRefresh() {
    // Esto es útil si quieres mostrar un botón de "Actualizar"
    if (confirm("Nueva versión disponible. ¿Recargar?")) {
      updateSW(true);
    }
  },
});

// 4. Configuración de rutas
const router = createBrowserRouter([
  {
    path: "/",
    Component: Layout,
    children: [
      { path: "", Component: Home },
      { path: "/aprender", Component: Learn },
    ],
  },
]);

// 5. Renderizado de la App
createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>,
);
