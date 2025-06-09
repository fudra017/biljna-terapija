//import { defineConfig } from 'vite'
//import react from '@vitejs/plugin-react'

// https://vite.dev/config/
////export default defineConfig({
//  plugins: [react()],
//})

import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

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