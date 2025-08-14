// src/api/api.js
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL, // npr. http://127.0.0.1:8000/api
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor za automatsko dodavanje Authorization header-a ako postoji token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('jwtToken');  // mora da se poklapa sa Login.jsx
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});

export default api;
