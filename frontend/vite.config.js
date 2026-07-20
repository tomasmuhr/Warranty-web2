import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    host: "0.0.0.0", // listen on all interfaces, not just localhost
    port: 5173,
    proxy: {
      '/api': {
        // target: 'http://localhost:8000',
        target: 'http://backend:8000',
        changeOrigin: true,
      },
    },
  },
})
