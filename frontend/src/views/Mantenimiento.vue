<template>
  
    <div class="maintenance-container">
      <div class="maintenance-header">
        <h1 class="maintenance-title">Gestión de Mantenimientos</h1>
        <button @click="openModal(null)" class="btn-add-maintenance">
          <i class="fas fa-plus"></i> Nuevo Mantenimiento
        </button>
      </div>

      <div class="table-container">
        <table class="maintenance-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Tipo</th>
              <th>Estado</th>
              <th class="long-text">Descripción</th>
              <th>Fecha Programada</th>
              <th>Responsable</th>
              <th>Dispositivos</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="mantenimiento in mantenimientos" :key="mantenimiento.id">
              <td>{{ mantenimiento.id }}</td>
              <td>{{ getTipoDisplay(mantenimiento.tipo) }}</td>
              <td>
                <span :class="['status-badge', `status-${mantenimiento.estado}`]">
                  {{ getEstadoDisplay(mantenimiento.estado) }}
                </span>
              </td>
              <td>{{ truncateText(mantenimiento.descripcion, 100) }}</td>
              <td>{{ formatDateTime(mantenimiento.fecha_programada) }}</td>
              <td>
                {{ mantenimiento.realizado_por ? mantenimiento.realizado_por.username : 'Sin asignar' }}
              </td>
              <td>{{ mantenimiento.dispositivos ? mantenimiento.dispositivos.length : 0 }}</td>
              <td>
                <div class="action-buttons">
                  <button @click="viewMaintenance(mantenimiento.id)" class="btn-action btn-view">
                    <i class="fas fa-eye"></i> Ver
                  </button>
                  <button @click="openModal(mantenimiento.id)" class="btn-action btn-edit">
                    <i class="fas fa-edit"></i> Editar
                  </button>
                  <button @click="confirmDelete(mantenimiento.id)" class="btn-action btn-delete">
                    <i class="fas fa-trash"></i> Eliminar
                  </button>
                </div>
              </td>
            </tr>
            <tr v-if="mantenimientos.length === 0">
              <td colspan="8" style="text-align: center;">No hay mantenimientos registrados</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Modal para agregar/editar mantenimiento -->
      <div v-if="showModal" class="modal-maintenance">
        <div class="modal-maintenance-content">
          <div class="modal-maintenance-header">
            <h2 class="modal-maintenance-title">{{ modalTitle }}</h2>
            <span @click="closeModal" class="close-modal">&times;</span>
          </div>
          
          <form @submit.prevent="submitForm" class="form-container">
            <input type="hidden" v-model="formData.id">
            
            <div class="form-row">
              <div class="form-col">
                <div class="form-group">
                  <label for="tipo">Tipo de Mantenimiento</label>
                  <select v-model="formData.tipo" class="form-control" required>
                    <option value="">Seleccione un tipo</option>
                    <option value="preventivo">Preventivo</option>
                    <option value="correctivo">Correctivo</option>
                  </select>
                </div>
              </div>
              <div class="form-col">
                <div class="form-group">
                  <label for="estado">Estado</label>
                  <select v-model="formData.estado" class="form-control" required>
                    <option value="programado">Programado</option>
                    <option value="en_proceso">En Proceso</option>
                    <option value="completado">Completado</option>
                    <option value="cancelado">Cancelado</option>
                  </select>
                </div>
              </div>
            </div>
            
            <div class="form-group">
              <label for="descripcion">Descripción</label>
              <textarea v-model="formData.descripcion" class="form-control" rows="3" required></textarea>
            </div>
            
            <div class="form-row">
              <div class="form-col">
                <div class="form-group">
                  <label for="fecha_programada">Fecha Programada</label>
                  <input type="datetime-local" v-model="formData.fecha_programada" class="form-control" required>
                </div>
              </div>
              <div class="form-col">
                <div class="form-group">
                  <label for="fecha_inicio">Fecha de Inicio (opcional)</label>
                  <input type="datetime-local" v-model="formData.fecha_inicio" class="form-control">
                </div>
              </div>
            </div>
            
            <div class="form-row">
              <div class="form-col">
                <div class="form-group">
                  <label for="fecha_fin">Fecha de Finalización (opcional)</label>
                  <input type="datetime-local" v-model="formData.fecha_fin" class="form-control">
                </div>
              </div>
              <div class="form-col">
                <div class="form-group">
                  <label for="realizado_por">Responsable</label>
                  <select v-model="formData.realizado_por" class="form-control">
                    <option value="">Seleccione un responsable</option>
                    <option v-for="usuario in usuarios" :key="usuario.id" :value="usuario.id">
                      {{ usuario.username }}
                    </option>
                  </select>
                </div>
              </div>
            </div>
            
            <div class="devices-selection">
              <h3>Dispositivos a Mantenimiento</h3>
              <div class="devices-list">
                <div v-for="dispositivo in dispositivos" :key="dispositivo.id" class="device-checkbox">
                  <input type="checkbox" :id="'device_' + dispositivo.id" 
                         v-model="formData.dispositivos" :value="dispositivo.id">
                  <label :for="'device_' + dispositivo.id">
                    {{ dispositivo.marca }} {{ dispositivo.modelo }} ({{ dispositivo.numero_inventario }})
                  </label>
                </div>
                <p v-if="dispositivos.length === 0">No hay dispositivos registrados</p>
              </div>
            </div>
            
            <div class="modal-maintenance-footer">
              <button type="button" @click="closeModal" class="btn-cancel">Cancelar</button>
              <button type="submit" class="btn-save">Guardar Mantenimiento</button>
            </div>
          </form>
        </div>
      </div>

      <!-- Modal para confirmar eliminación -->
      <div v-if="showDeleteModal" class="modal-maintenance">
        <div class="modal-maintenance-content" style="max-width: 500px;">
          <div class="modal-maintenance-header">
            <h2 class="modal-maintenance-title">Confirmar Eliminación</h2>
            <span @click="closeDeleteModal" class="close-modal">&times;</span>
          </div>
          
          <p>¿Está seguro que desea eliminar este mantenimiento? Esta acción no se puede deshacer.</p>
          
          <div class="modal-maintenance-footer">
            <button type="button" @click="closeDeleteModal" class="btn-cancel">Cancelar</button>
            <button type="button" @click="deleteMaintenance" class="btn-save" style="background-color: #F44336;">
              Eliminar
            </button>
          </div>
        </div>
      </div>
    </div>
</template>

<script>
import DashboardLayout from '@/layouts/Layout.vue';
import axios from 'axios';

export default {
  name: 'Mantenimiento',
  components: {
    DashboardLayout
  },
  data() {
    return {
      mantenimientos: [],
      dispositivos: [],
      usuarios: [],
      showModal: false,
      showDeleteModal: false,
      currentMaintenanceId: null,
      formData: {
        id: '',
        tipo: '',
        estado: 'programado',
        descripcion: '',
        fecha_programada: '',
        fecha_inicio: '',
        fecha_fin: '',
        realizado_por: '',
        dispositivos: []
      }
    };
  },
  computed: {
    modalTitle() {
      return this.currentMaintenanceId ? 'Editar Mantenimiento' : 'Nuevo Mantenimiento';
    }
  },
  async created() {
    await this.fetchData();
  },
  methods: {
    async fetchData() {
      try {
        const [mantenimientosRes, dispositivosRes, usuariosRes] = await Promise.all([
          axios.get('/api/mantenimientos/'),
          axios.get('/api/dispositivos/'),
          axios.get('/api/usuarios/')
        ]);
        
        this.mantenimientos = mantenimientosRes.data;
        this.dispositivos = dispositivosRes.data;
        this.usuarios = usuariosRes.data;
      } catch (error) {
        console.error('Error fetching data:', error);
        this.showError('Error al cargar los datos');
      }
    },
    
    getTipoDisplay(tipo) {
      const tipos = {
        'preventivo': 'Preventivo',
        'correctivo': 'Correctivo'
      };
      return tipos[tipo] || tipo;
    },
    
    getEstadoDisplay(estado) {
      const estados = {
        'programado': 'Programado',
        'en_proceso': 'En Proceso',
        'completado': 'Completado',
        'cancelado': 'Cancelado'
      };
      return estados[estado] || estado;
    },
    
    truncateText(text, length) {
      return text?.length > length ? text.substring(0, length) + '...' : text;
    },
    
    formatDateTime(dateTimeStr) {
      if (!dateTimeStr) return '';
      const date = new Date(dateTimeStr);
      return date.toLocaleString('es-ES', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    },
    
    async openModal(maintenanceId) {
      this.currentMaintenanceId = maintenanceId;
      
      if (maintenanceId) {
        try {
          const response = await axios.get(`/api/mantenimientos/${maintenanceId}/`);
          const data = response.data;
          
          this.formData = {
            id: data.id,
            tipo: data.tipo,
            estado: data.estado,
            descripcion: data.descripcion,
            fecha_programada: this.formatDateTimeForInput(data.fecha_programada),
            fecha_inicio: this.formatDateTimeForInput(data.fecha_inicio),
            fecha_fin: this.formatDateTimeForInput(data.fecha_fin),
            realizado_por: data.realizado_por?.id || '',
            dispositivos: data.dispositivos?.map(d => d.id) || []
          };
        } catch (error) {
          console.error('Error fetching maintenance:', error);
          this.showError('Error al cargar el mantenimiento');
          return;
        }
      } else {
        this.resetForm();
      }
      
      this.showModal = true;
    },
    
    formatDateTimeForInput(dateTimeStr) {
      if (!dateTimeStr) return '';
      const date = new Date(dateTimeStr);
      const isoString = date.toISOString();
      return isoString.substring(0, 16); // Formato YYYY-MM-DDTHH:MM
    },
    
    resetForm() {
      this.formData = {
        id: '',
        tipo: '',
        estado: 'programado',
        descripcion: '',
        fecha_programada: '',
        fecha_inicio: '',
        fecha_fin: '',
        realizado_por: '',
        dispositivos: []
      };
    },
    
    closeModal() {
      this.showModal = false;
      this.currentMaintenanceId = null;
    },
    
    viewMaintenance(id) {
      // Implementar vista detallada
      alert(`Ver mantenimiento ${id}`);
    },
    
    confirmDelete(id) {
      this.currentMaintenanceId = id;
      this.showDeleteModal = true;
    },
    
    closeDeleteModal() {
      this.showDeleteModal = false;
      this.currentMaintenanceId = null;
    },
    
    async deleteMaintenance() {
      if (!this.currentMaintenanceId) return;
      
      try {
        await axios.delete(`/api/mantenimientos/${this.currentMaintenanceId}/`);
        this.showSuccess('Mantenimiento eliminado correctamente');
        await this.fetchData();
      } catch (error) {
        console.error('Error deleting maintenance:', error);
        this.showError('Error al eliminar el mantenimiento');
      }
      
      this.closeDeleteModal();
    },
    
    async submitForm() {
      try {
        const url = this.currentMaintenanceId 
          ? `/api/mantenimientos/${this.currentMaintenanceId}/` 
          : '/api/mantenimientos/';
        
        const method = this.currentMaintenanceId ? 'put' : 'post';
        
        await axios[method](url, this.formData);
        this.showSuccess(
          this.currentMaintenanceId 
            ? 'Mantenimiento actualizado correctamente' 
            : 'Mantenimiento creado correctamente'
        );
        
        await this.fetchData();
        this.closeModal();
      } catch (error) {
        console.error('Error saving maintenance:', error);
        this.showError(
          error.response?.data?.message || 
          'Error al guardar el mantenimiento'
        );
      }
    },
    
    showSuccess(message) {
      alert(message); // Puedes reemplazar esto con un sistema de notificaciones más elegante
    },
    
    showError(message) {
      alert(message); // Puedes reemplazar esto con un sistema de notificaciones más elegante
    }
  }
};
</script>

<style scoped>
.maintenance-container {
  padding: 2rem;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  margin-bottom: 20px;
}

.maintenance-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

.maintenance-title {
  font-size: 1.5rem;
  color: var(--primary-dark);
}

.btn-add-maintenance {
  background-color: var(--accent-green);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  font-size: 0.9rem;
  cursor: pointer;
  border: none;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
}

.btn-add-maintenance:hover {
  background-color: var(--primary-green-dark);
  transform: translateY(-2px);
}

.table-container {
  width: 100%;
  overflow-x: auto;
  margin-bottom: 20px;
  border: 1px solid #eee;
  border-radius: 4px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.maintenance-table {
  width: 100%;
  min-width: 800px;
  border-collapse: collapse;
  white-space: nowrap;
}

.maintenance-table th {
  background-color: #f5f5f5;
  padding: 12px;
  text-align: left;
  font-weight: 600;
  position: sticky;
  top: 0;
}

.maintenance-table td {
  padding: 12px;
  border-bottom: 1px solid #eee;
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
}

.maintenance-table td.long-text {
  white-space: normal;
  max-width: 300px;
}

.maintenance-table tr:hover {
  background-color: #f9f9f9;
}

.status-badge {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 500;
}

.status-programado {
  background-color: #FFF3E0;
  color: #E65100;
}

.status-en_proceso {
  background-color: #E3F2FD;
  color: #0D47A1;
}

.status-completado {
  background-color: #E8F5E9;
  color: #2E7D32;
}

.status-cancelado {
  background-color: #FFEBEE;
  color: #C62828;
}

.action-buttons {
  display: flex;
  gap: 8px;
}

.btn-action {
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 0.8rem;
  cursor: pointer;
  border: none;
  display: flex;
  align-items: center;
  gap: 4px;
  transition: all 0.3s ease;
}

.btn-edit {
  background-color: #2196F3;
  color: white;
}

.btn-edit:hover {
  background-color: #0D47A1;
}

.btn-delete {
  background-color: #F44336;
  color: white;
}

.btn-delete:hover {
  background-color: #C62828;
}

.btn-view {
  background-color: #4CAF50;
  color: white;
}

.btn-view:hover {
  background-color: #2E7D32;
}

.modal-maintenance {
  position: fixed;
  z-index: 2000;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0,0,0,0.5);
  overflow: auto;
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-maintenance-content {
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  width: 90%;
  max-width: 800px;
  max-height: 90vh;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  overflow-y: auto;
}

.modal-maintenance-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

.modal-maintenance-title {
  font-size: 1.3rem;
  color: var(--primary-dark);
}

.close-modal {
  font-size: 1.5rem;
  cursor: pointer;
  color: #777;
  transition: color 0.3s ease;
}

.close-modal:hover {
  color: #333;
}

.form-container {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-row {
  display: flex;
  gap: 1.5rem;
}

.form-col {
  flex: 1;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: var(--primary-dark);
}

.form-control {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

.form-control:focus {
  border-color: var(--accent-green);
  outline: none;
  box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2);
}

textarea.form-control {
  min-height: 100px;
  resize: vertical;
}

.devices-selection {
  border: 1px solid #eee;
  padding: 1rem;
  border-radius: 8px;
}

.devices-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
  max-height: 50vh;
  overflow-y: auto;
  padding: 0.5rem;
}

.device-checkbox {
  margin-bottom: 0.5rem;
}

.device-checkbox input[type="checkbox"] {
  margin-right: 0.5rem;
}

.modal-maintenance-footer {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid #eee;
}

.btn-save {
  background-color: var(--accent-green);
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-save:hover {
  background-color: var(--primary-green-dark);
  transform: translateY(-2px);
}

.btn-cancel {
  background-color: #f5f5f5;
  color: #333;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  border: 1px solid #ddd;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-cancel:hover {
  background-color: #e0e0e0;
}

/* Barra de scroll personalizada */
.table-container::-webkit-scrollbar {
  height: 8px;
}

.table-container::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.table-container::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

.table-container::-webkit-scrollbar-thumb:hover {
  background: #555;
}

/* Responsive */
@media (max-width: 768px) {
  .maintenance-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .form-row {
    flex-direction: column;
    gap: 1rem;
  }
  
  .modal-maintenance-content {
    width: 95%;
    margin: 1rem auto;
  }
  
  .devices-list {
    grid-template-columns: 1fr;
  }
}
</style>