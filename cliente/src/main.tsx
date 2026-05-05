import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import { createBrowserRouter } from "react-router";
import { RouterProvider } from "react-router/dom";

// 1. Imports de tus componentes
import Home from './views/Home'
import Scaffold from './components/Scaffold'
import TopBar from './components/TopBar'
import BottomBar from './components/BottomBar'

// 2. Registro del Service Worker (Importación Virtual)
import { registerSW } from 'virtual:pwa-register'

// 3. Ejecución inmediata del registro
const updateSW = registerSW({
  onOfflineReady() {
    console.log('App lista para trabajar offline');
  },
  onNeedRefresh() {
    // Esto es útil si quieres mostrar un botón de "Actualizar"
    if (confirm('Nueva versión disponible. ¿Recargar?')) {
      updateSW(true);
    }
  },
});

// 4. Configuración de rutas
const router = createBrowserRouter([
  {
    path: "/",
    children: [
      {path: "", Component: Home}
    ]
  },
]);

// 5. Renderizado de la App
createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>,
)
