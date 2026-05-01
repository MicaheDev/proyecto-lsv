import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import { VitePWA } from 'vite-plugin-pwa'

// https://vite.dev/config/
export default defineConfig({
  base: "/",
  plugins: [react(), 
  tailwindcss(),
VitePWA({
  registerType: 'autoUpdate',
  includeAssets: ['icon-192.png', 'icon-512.png'], // Dile a Vite que incluya estos recursos
  manifest: {
    name: 'LSV Aprendizaje',
    short_name: 'LSV',
    description: 'Sistema de aprendizaje de Lengua de Señas Venezolana', // Recomendado
    theme_color: '#ef4444',
    background_color: '#ffffff', // Color de fondo al abrir la app
    display: 'standalone',       // ESTO ES LO QUE ACTIVA EL MODO APP
start_url: '/',
scope: '/',
    icons: [
      {
        src: 'icon-192.png',     // Sin el prefijo public/, solo el nombre
        sizes: '192x192',
        type: 'image/png',
        purpose: 'any'           // Recomendado para mejor compatibilidad
      },
      {
        src: 'icon-512.png',
        sizes: '512x512',
        type: 'image/png',
        purpose: 'any'
      }
    ]
  }
})

  
  ],
})
