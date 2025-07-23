<template>
    <div class="inventario-container">
      <div class="add-device-form glass-card">
        <h3 class="form-title">Agregar Nuevo Dispositivo</h3>
        
        <div v-if="messages.length" class="messages">
          <div v-for="(message, index) in messages" :key="index" 
               :class="['alert', message.type ? 'alert-' + message.type : '']">
            {{ message.text }}
          </div>
        </div>
        
        <form @submit.prevent="submitForm" class="device-form">
          <!-- Primera fila: N° Inventario + Modelo -->
          <div class="form-row">
            <div class="form-group half-width">
              <label for="inventory_number">N° de Inventario:</label>
              <input type="text" id="inventory_number" v-model="formData.inventory_number" 
                     class="form-control" required 
                     pattern="[A-Za-z0-9-]+" title="Solo letras, números y guiones">
            </div>
            
            <div class="form-group half-width">
              <label for="model">Modelo:</label>
              <input type="text" id="model" v-model="formData.model" class="form-control" required>
            </div>
          </div>
          
          <!-- Segunda fila: Tipo + Marca -->
          <div class="form-row">
            <div class="form-group half-width">
              <label for="tipo">Tipo:</label>
              <select id="tipo" v-model="formData.tipo" class="form-control" required>
                <option value="">Seleccione un tipo</option>
                <option value="computadora">Computadora</option>
                <option value="movil">Móvil</option>
                <option value="telefono_fijo">Teléfono Fijo</option>
                <option value="impresora">Impresora</option>
                <option value="router">Router</option>
                <option value="switcher">Switcher</option>
                <option value="otro">Otro</option>
              </select>
            </div>

            <div class="form-group half-width">
              <label for="brand">Marca:</label>
              <select id="brand" v-model="formData.brand" class="form-control" required>
                <option value="">Seleccione una marca</option>
                <option value="Dell">Dell</option>
                <option value="HP">HP</option>
                <option value="Lenovo">Lenovo</option>
                <option value="Apple">Apple</option>
                <option value="Asus">Asus</option>
                <option value="Acer">Acer</option>
                <option value="Otro">Otro</option>
              </select>
            </div>
          </div>
          
          <!-- Tercera fila: Número de Serie + Ubicación -->
          <div class="form-row">
            <div class="form-group half-width">
              <label for="serial_number">Número de Serie:</label>
              <input type="text" id="serial_number" v-model="formData.serial_number" 
                     class="form-control" required>
            </div>
            
            <div class="form-group half-width">
              <label for="location">Ubicación:</label>
              <select id="location" v-model="formData.location" class="form-control" required>
                <option value="">Seleccione una ubicación</option>
                <option value="Departamento de Sistema">Departamento de Sistema</option>
                <option value="Gerencia Financiera">Gerencia Financiera</option>
                <option value="Seguridad y Proteccion">Seguridad y Protección</option>
                <option value="Atención al hombre">Atención al hombre</option>
                <option value="Auditoria">Auditoría</option>
              </select>
            </div>
          </div>
          
          <!-- Cuarta fila: Fecha + Estado -->
          <div class="form-row">
            <div class="form-group half-width">
              <label for="acquisition_date">Fecha de Adquisición:</label>
              <input type="date" id="acquisition_date" v-model="formData.acquisition_date" 
                     class="form-control" required>
            </div>
            
            <div class="form-group half-width">
              <label for="status">Estado:</label>
              <select id="status" v-model="formData.status" class="form-control" required>
                <option value="">Seleccione un estado</option>
                <option value="Activo">Activo</option>
                <option value="En reparación">En reparación</option>
                <option value="Baja">Baja</option>
              </select>
            </div>
          </div>
          
          <!-- Quinta fila: Responsable (ocupará toda la fila) -->
          <div class="form-row">
            <div class="form-group full-width">
              <label for="responsable">Responsable:</label>
              <select id="responsable" v-model="formData.responsable" class="form-control">
                <option value="">Seleccione un responsable</option>
                <option v-for="usuario in usuarios" :key="usuario.id" :value="usuario.id">
                  {{ usuario.full_name || usuario.username }} ({{ usuario.role }})
                </option>
              </select>
            </div>
          </div>
          
          <button type="submit" class="btn-submit">Guardar Dispositivo</button>
        </form>
      </div>
    </div>
</template>

<script>
import DashboardLayout from '@/layouts/Layout.vue';
import axios from 'axios';

export default {
  name: 'Inventario',
  components: {
    DashboardLayout
  },
  data() {
    return {
      formData: {
        inventory_number: '',
        model: '',
        tipo: '',
        brand: '',
        serial_number: '',
        location: '',
        acquisition_date: '',
        status: '',
        responsable: ''
      },
      usuarios: [],
      messages: []
    };
  },
  async created() {
    await this.fetchUsuarios();
  },
  methods: {
    async fetchUsuarios() {
      try {
        const response = await axios.get('/api/usuarios/');
        this.usuarios = response.data;
      } catch (error) {
        console.error('Error fetching usuarios:', error);
        this.messages.push({
          type: 'error',
          text: 'Error al cargar la lista de usuarios'
        });
      }
    },
    async submitForm() {
      try {
        const response = await axios.post('/api/dispositivos/', this.formData);
        
        this.messages.push({
          type: 'success',
          text: '✅ Dispositivo agregado correctamente!'
        });
        
        this.formData = {
          inventory_number: '',
          model: '',
          tipo: '',
          brand: '',
          serial_number: '',
          location: '',
          acquisition_date: '',
          status: '',
          responsable: ''
        };
        
        setTimeout(() => {
          this.messages = [];
        }, 5000);
        
      } catch (error) {
        console.error('Error al guardar dispositivo:', error);
        
        let errorMessage = '❌ Error al guardar el dispositivo';
        if (error.response && error.response.data) {
          errorMessage += `: ${error.response.data.message || JSON.stringify(error.response.data)}`;
        }
        
        this.messages.push({
          type: 'error',
          text: errorMessage
        });
      }
    }
  }
};
</script>

<style scoped>
.inventario-container {
  padding: 2rem;
  animation: fadeIn 0.5s ease-out;
}

.add-device-form {
  max-width: 800px; /* Aumentado de 600px */
  margin: 0 auto;
  padding: 2rem;
  border-radius: 12px;
}

.form-title {
  text-align: center;
  margin-bottom: 1.5rem;
  color: var(--primary-dark);
}

.device-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-row {
  display: flex;
  gap: 1.5rem;
  width: 100%;
}

.form-group {
  margin-bottom: 0;
}

.half-width {
  flex: 1;
  min-width: 0;
}

.full-width {
  width: 100%;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: var(--primary-dark);
}

.form-control {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  background-color: white;
  transition: border-color 0.3s ease;
}

.form-control:focus {
  border-color: var(--accent-green);
  outline: none;
  box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2);
}

select.form-control {
  height: auto;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' fill='%23212121' viewBox='0 0 16 16'%3E%3Cpath d='M7.247 11.14 2.451 5.658C1.885 5.013 2.345 4 3.204 4h9.592a1 1 0 0 1 .753 1.659l-4.796 5.48a1 1 0 0 1-1.506 0z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 0.75rem center;
  background-size: 16px 12px;
}

.btn-submit {
  background-color: var(--accent-green);
  color: white;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  width: 100%;
  transition: all 0.3s ease;
  margin-top: 0.5rem;
}

.btn-submit:hover {
  background-color: var(--primary-green-dark);
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.messages {
  margin-bottom: 1.5rem;
}

.alert {
  padding: 1rem;
  margin-bottom: 1rem;
  border-radius: 8px;
  font-weight: 500;
}

.alert-success {
  background-color: rgba(212, 237, 218, 0.9);
  color: #155724;
  border: 1px solid #c3e6cb;
}

.alert-error {
  background-color: rgba(248, 215, 218, 0.9);
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.glass-card {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1);
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 768px) {
  .inventario-container {
    padding: 1rem;
  }
  
  .add-device-form {
    padding: 1.5rem;
  }
  
  .form-row {
    flex-direction: column;
    gap: 1rem;
  }
  
  .half-width, .full-width {
    width: 100%;
  }
}
</style>