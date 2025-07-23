<template>
  <div class="user-management">
    <h2>Gestión de Usuarios</h2>
    
    <!-- Formulario de creación -->
    <form @submit.prevent="handleSubmit" class="custom-form">
      <input type="hidden" v-model="formData.id">
      
      <div class="form-grid">
        <!-- Fila 1 -->
        <div class="form-group">
          <label for="firstName">Nombre</label>
          <input type="text" id="firstName" v-model="formData.first_name" class="form-control" required>
        </div>
        <div class="form-group">
          <label for="lastName">Apellidos</label>
          <input type="text" id="lastName" v-model="formData.last_name" class="form-control" required>
        </div>
        
        <!-- Fila 2 -->
        <div class="form-group">
          <label for="id">Carnet de Identidad</label>
          <input type="text" id="id" v-model="formData.id" class="form-control" required>
        </div>
        <div class="form-group">
          <label for="username">Usuario</label>
          <input type="text" id="username" v-model="formData.username" class="form-control" required>
        </div>
        
        <!-- Fila 3 -->
        <div class="form-group">
          <label for="email">Email</label>
          <input type="email" id="email" v-model="formData.email" class="form-control" required>
        </div>
        <div class="form-group">
          <label for="role">Rol</label>
          <select id="role" v-model="formData.role" class="form-select" required>
            <option value="">Seleccionar...</option>
            <option value="superadmin">Super Admin</option>
            <option value="admin">Admin</option>
            <option value="invitado">Invitado</option>
          </select>
        </div>
        
        <!-- Fila 4 -->
        <div class="form-group">
          <label for="password">Contraseña</label>
          <input type="password" id="password" v-model="formData.password" class="form-control" :required="!formData.id">
        </div>
        <div class="form-group">
          <label for="confirmPassword">Confirmar contraseña</label>
          <input 
            type="password" 
            id="confirmPassword" 
            v-model="confirmPassword" 
            class="form-control" 
            :required="!formData.id"
            :class="{ 'is-invalid': passwordMismatch }"
          >
          <div v-if="passwordMismatch" class="invalid-feedback">Las contraseñas no coinciden</div>
        </div>
      </div>

      <div class="form-actions">
        <button type="submit" class="btn btn-save">{{ formData.internal_id ? 'Actualizar' : 'Guardar' }}</button>
        <button v-if="formData.id" type="button" class="btn btn-cancel" @click="resetForm">Cancelar</button>
      </div>
    </form>

    <!-- Tabla de usuarios -->
    <div class="table-responsive">
      <table class="custom-table">
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Email</th>
            <th>Rol</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.first_name }} {{ user.last_name }}</td>
            <td>{{ user.email }}</td>
            <td>{{ getRoleDisplay(user.role) }}</td>
            <td>
              <button class="btn-edit" @click="editUser(user)">Editar</button>
              <button class="btn-delete" @click="deleteUser(user.id)">Eliminar</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import DashboardLayout from '@/layouts/Layout.vue'
export default {
    name: 'Usuarios',
    components:{
        DashboardLayout
    },
  setup() {
    const users = ref([])
    const formData = ref({
    id: '',          // Carnet de identidad (visible)
    internal_id: '', // ID interno (hidden, para actualizaciones)
    first_name: '',
    last_name: '',
    username: '',
    email: '',
    role: '',
    password: ''
    })
    const confirmPassword = ref('')
    
    // Computed para validación de contraseñas
    const passwordMismatch = computed(() => {
      return formData.value.password && confirmPassword.value && 
             formData.value.password !== confirmPassword.value
    })
    
    // Obtener lista de usuarios
    const fetchUsers = async () => {
      try {
        const response = await axios.get('/api/users/', {
            withCredentials: true
        })
        users.value = response.data
      } catch (error) {
        console.error('Error al cargar usuarios:', error)
      }
    }
    
    // Mostrar texto del rol
    const getRoleDisplay = (role) => {
      const roles = {
        'superadmin': 'Super Admin',
        'admin': 'Admin',
        'invitado': 'Invitado'
      }
      return roles[role] || role
    }
    
    // Manejar envío del formulario
    const handleSubmit = async () => {
  // Validación mejorada
  if (!formData.value.id) {
    alert("El carnet de identidad es obligatorio")
    return
  }
  
  if (!formData.value.internal_id && !formData.value.password) {
    alert("La contraseña es obligatoria para nuevos usuarios")
    return
  }

  if (passwordMismatch.value) {
    return
  }

  try {
    const isUpdate = !!formData.value.internal_id
    const url = isUpdate 
      ? `/api/users/${formData.value.internal_id}/` 
      : '/api/users/'
    
    const method = isUpdate ? 'put' : 'post'

    // Preparamos los datos a enviar
    const payload = {
      id: formData.value.id, // Carnet de identidad
      first_name: formData.value.first_name,
      last_name: formData.value.last_name,
      username: formData.value.username,
      email: formData.value.email,
      role: formData.value.role,
      ...(!isUpdate && { password: formData.value.password }) // Solo envía password en creación
    }

    const response = await axios({
      method,
      url,
      data: payload,
      headers: {
        'X-CSRFToken': getCookie('csrftoken'),
        'Content-Type': 'application/json'
      }
    })

    resetForm()
    await fetchUsers()
    alert(isUpdate ? 'Usuario actualizado' : 'Usuario creado')
    
  } catch (error) {
    console.error('Error:', error.response?.data || error)
    alert(`Error: ${error.response?.data?.detail || 'Ocurrió un error'}`)
  }
}

// Modifica editUser:
const editUser = (user) => {
  formData.value = {
    id: user.id,          // Carnet de identidad
    internal_id: user.id, // ID interno para actualización
    first_name: user.first_name,
    last_name: user.last_name,
    username: user.username,
    email: user.email,
    role: user.role,
    password: ''          // No mostramos la contraseña existente
  }
  confirmPassword.value = ''
}
    
    // Eliminar usuario
    const deleteUser = async (id) => {
      if (confirm('¿Eliminar este usuario?')) {
        try {
          await axios.delete(`/api/users/${id}/`, {
            headers: {
              'X-CSRFToken': getCookie('csrftoken')
            }
          })
          await fetchUsers()
        } catch (error) {
          console.error('Error al eliminar usuario:', error)
        }
      }
    }
    
    // Resetear formulario
    const resetForm = () => {
      formData.value = {
        id: '',
        first_name: '',
        last_name: '',
        username: '',
        email: '',
        role: '',
        password: ''
      }
      confirmPassword.value = ''
    }
    
    // Helper para obtener cookies
    const getCookie = (name) => {
      let cookieValue = null
      if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';')
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim()
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
            break
          }
        }
      }
      return cookieValue
    }
    
    // Cargar usuarios al montar el componente
    onMounted(fetchUsers)
    
    return {
      users,
      formData,
      confirmPassword,
      passwordMismatch,
      fetchUsers,
      getRoleDisplay,
      handleSubmit,
      editUser,
      deleteUser,
      resetForm
    }
  }
}
</script>

<style scoped>
.user-management {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.custom-form {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 30px;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
  margin-bottom: 15px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-control, .form-select {
  padding: 10px;
  border: 1px solid #ced4da;
  border-radius: 4px;
  font-size: 16px;
}

.form-control.is-invalid {
  border-color: #dc3545;
}

.invalid-feedback {
  color: #dc3545;
  font-size: 0.875em;
  margin-top: 0.25rem;
}

.custom-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.custom-table th, .custom-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #dee2e6;
}

.custom-table th {
  background-color: #f8f9fa;
  font-weight: 600;
}

.btn-save, .btn-cancel {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  margin-right: 10px;
}

.btn-save {
  background-color: #4CAF50;
  color: white;
}

.btn-save:hover {
  background-color: #3e8e41;
}

.btn-cancel {
  background-color: #6c757d;
  color: white;
}

.btn-cancel:hover {
  background-color: #5a6268;
}

.btn-edit, .btn-delete {
  padding: 5px 10px;
  margin-right: 5px;
  border-radius: 3px;
  cursor: pointer;
  border: none;
}

.btn-edit {
  background-color: #2196F3;
  color: white;
}

.btn-edit:hover {
  background-color: #0b7dda;
}

.btn-delete {
  background-color: #f44336;
  color: white;
}

.btn-delete:hover {
  background-color: #da190b;
}

.table-responsive {
  overflow-x: auto;
}

@media (max-width: 768px) {
  .form-grid {
    grid-template-columns: 1fr;
  }
}
</style>