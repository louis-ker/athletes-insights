import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Pour éviter les erreurs CORS en dev local, on peut ajouter un proxy :
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': 'https://athletes-insights-backend.onrender.com/api/hello'
    }
  },
  build: {
    outDir: 'dist',
  }
})