import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// O frontend fala com a API pela própria origem (/api) e o dev server faz o
// proxy para o container da API — assim não há CORS nem cookie cross-site.
const apiTarget = process.env.API_URL || 'http://localhost:8000'

export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    port: 3000,
    strictPort: true,
    // Bind mount pode não emitir eventos de inotify no sandbox: em modo preview
    // o watcher usa polling (o host define BASE44_PREVIEW_MODE=1).
    watch: { usePolling: process.env.BASE44_PREVIEW_MODE === '1' },
    proxy: {
      '/api': { target: apiTarget, changeOrigin: true },
    },
  },
})
