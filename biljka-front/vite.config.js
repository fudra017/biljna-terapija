import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path'; // ⬅⬅⬅ OBAVEZNO

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'), // ⬅⬅⬅ Alias za @
    },
  },
  build: {
    outDir: 'dist', // Netlify očekuje ovaj folder
  },
  server: {
    port: 3000,
    open: true,
  },
});
