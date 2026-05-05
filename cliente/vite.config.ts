import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";
import { VitePWA } from "vite-plugin-pwa";

// https://vite.dev/config/
export default defineConfig({
  base: "/",
  plugins: [
    react(),
    tailwindcss(),
    VitePWA({
      filename: 'manifest.json', // Fuerza el nombre que el navegador está buscando
      registerType: "autoUpdate",
      includeAssets: ['favicon.svg', 'icon-192x192.png', 'icon-512x512.png'],
      injectRegister: "script", // Esto ayuda a que se registre el SW automáticamente
      workbox: {
        globPatterns: ["**/*.{js,css,html,ico,png,svg}"], // Cachea estos archivos
      },
      manifest: {
        name: "LSV Aprendizaje",
        short_name: "LSV",
        description: "Sistema de aprendizaje de Lengua de Señas Venezolana", // Recomendado
        theme_color: "#ef4444",
        background_color: "#ffffff", // Color de fondo al abrir la app
        display: "standalone", // ESTO ES LO QUE ACTIVA EL MODO APP
        start_url: "/",
        scope: "/",
        icons: [
          {
            src: "icon-192x192.png", // <--- Cambiado para coincidir con tu 'ls'
            sizes: "192x192",
            type: "image/png",
            purpose: "any",
          },
          {
            src: "icon-512x512.png", // <--- Cambiado para coincidir con tu 'ls'
            sizes: "512x512",
            type: "image/png",
            purpose: "any",
          },
          // Te sugiero añadir los maskable que ya tienes para que se vea bien en Android
          {
            src: "icon-192x192-maskable.png",
            sizes: "192x192",
            type: "image/png",
            purpose: "maskable",
          },
        ],
      },
    }),
  ],
});
