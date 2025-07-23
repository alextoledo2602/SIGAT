import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/',
  withCredentials: true,
  headers: {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'X-Requested-With': 'XMLHttpRequest'
  }
})

// Interceptor para manejar CSRF
api.interceptors.request.use(async (config) => {
  // Solo para métodos que modifican datos
  if (['post', 'put', 'patch', 'delete'].includes(config.method.toLowerCase())) {
    try {
      await axios.get(`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/auth/csrf/`, {
        withCredentials: true
      })
    } catch (error) {
      console.error('Error obteniendo CSRF token:', error)
      throw error
    }
  }
  return config
})

export default api