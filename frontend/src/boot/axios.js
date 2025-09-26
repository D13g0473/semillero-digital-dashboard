import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:5001/api', // URL base de nuestro backend
  withCredentials: true, // Importante para que envíe las cookies de sesión
});

export { api };
