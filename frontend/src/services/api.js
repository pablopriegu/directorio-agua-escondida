import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api'
});

// Interceptor para añadir el token a las cabeceras
api.interceptors.request.use(config => {
  const authTokens = localStorage.getItem('authTokens');
  if (authTokens) {
    const token = JSON.parse(authTokens).access;
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;