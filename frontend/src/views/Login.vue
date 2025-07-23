<template>
  <div class="login-page">
    <div class="login-container">
      <h2>Iniciar sesión</h2>
      
      <div v-if="error" class="alert-error">
        {{ errorMessage }}
      </div>
      
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="username">Usuario:</label>
          <input 
            type="text" 
            id="username" 
            v-model="credentials.username" 
            required 
            autofocus
          >
        </div>
        
        <div class="form-group">
          <label for="password">Contraseña:</label>
          <input 
            type="password" 
            id="password" 
            v-model="credentials.password" 
            required
          >
        </div>
        
        <button type="submit" class="btn-login" :disabled="loading">
          {{ loading ? 'Ingresando...' : 'Ingresar' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from '@/plugins/axios'

export default {
  data() {
    return {
      credentials: {
        username: '',
        password: ''
      },
      error: false,
      errorMessage: '',
      loading: false,
    }
  },
  methods: {
    getCSRFToken() {
      const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
      return cookieValue;
    },

    async handleLogin() {
      this.loading = true;
      this.error = false;
      this.errorMessage = '';
      
      try {
        // 1. Obtener CSRF Token
        await axios.get('/api/auth/csrf/', { withCredentials: true });

        // 2. Hacer login
        const response = await axios.post('/api/login/', 
          {
            username: this.credentials.username, // Corregido: usar credentials
            password: this.credentials.password
          }, 
          {
            headers: {
              'X-CSRFToken': this.getCSRFToken(), // Corregido: nombre del método
              'Content-Type': 'application/json'
            },
            withCredentials: true
          }
        );

        console.log("Login exitoso:", response.data);
        // Redirección o manejo de éxito aquí
        window.location.href = '/dashboard';
      } catch (error) {
        console.error("Error en login:", error);
        this.error = true;
        this.errorMessage = error.response?.data?.message || 
                          'Error al iniciar sesión. Por favor intente nuevamente.';
        
        if (error.response?.status === 401) {
          this.errorMessage = 'Usuario o contraseña incorrectos';
        }
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>

<style scoped>
/* Tus estilos actuales se mantienen igual */
.login-page {
  background: url('/static/images/background-login.png') no-repeat center center fixed;
  background-size: cover;
  min-height: 100vh;
  margin: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  z-index: 0;
}

.login-container {
  max-width: 300px;
  width: 100%;
  padding: 2.5rem;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  background-color: rgba(255, 255, 255, 0.8);
  z-index: 2;
}

.login-container h2 {
  text-align: center;
  color: #000000; 
  margin-bottom: 1.8rem;
  font-weight: 700;
  font-size: 1.8rem;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  color: #333333;
  font-weight: 500;
  font-size: 0.95rem;
}

.form-group input {
  padding: 0.85rem 1rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.form-group input:focus {
  border-color: #000000;
  outline: none;
  box-shadow: 0 0 0 3px rgba(46, 125, 50, 0.2);
}

.btn-login {
  background-color: #000000;
  color: white;
  padding: 0.9rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  transition: all 0.3s ease;
  margin-top: 0.5rem;
}

.btn-login:hover {
  background-color: #3d3d3d;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.btn-login:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.alert-error {
  color: #d32f2f;
  background-color: #ffebee;
  padding: 0.8rem;
  border-radius: 6px;
  margin-bottom: 1rem;
  text-align: center;
  border-left: 4px solid #d32f2f;
}
</style>