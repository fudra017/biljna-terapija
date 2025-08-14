import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path'  // <-- Ovo je neophodno za alias

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'dist', // Netlify očekuje ovaj folder
  },
  server: {
    port: 3000,
    open: true,
  },
});
