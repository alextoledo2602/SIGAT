<template>
  <div class="backup-list">
    <h3><i class="fas fa-history"></i> Historial de Backups</h3>
    
    <div class="backup-filters">
      <form @submit.prevent="applyFilters" class="filter-form">
        <div class="form-row">
          <div class="form-group">
            <label for="filter-type">Filtrar por tipo:</label>
            <select id="filter-type" v-model="filterType">
              <option value="">Todos los tipos</option>
              <option value="completo">Completo</option>
              <option value="diferencial">Diferencial</option>
              <option value="incremental">Incremental</option>
            </select>
          </div>
          
          <div class="form-group">
            <label for="filter-date">Filtrar por fecha:</label>
            <input type="date" id="filter-date" v-model="filterDate">
          </div>
          
          <div class="form-group">
            <label for="filter-user">Filtrar por usuario:</label>
            <select id="filter-user" v-model="filterUser">
              <option value="">Todos los usuarios</option>
              <option v-for="user in users" :key="user.id" :value="user.id">
                {{ user.username }}
              </option>
            </select>
          </div>
        </div>
        
        <div class="form-actions">
          <button type="submit" class="btn-filter">
            <i class="fas fa-filter"></i> Filtrar
          </button>
          <button type="reset" class="btn-reset" @click="resetFilters">
            <i class="fas fa-undo"></i> Limpiar
          </button>
        </div>
      </form>
    </div>
    
    <div class="table-responsive">
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Fecha Creación</th>
            <th>Tipo</th>
            <th>Descripción</th>
            <th>Tamaño</th>
            <th>Ubicación</th>
            <th>Creado por</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="backup in filteredBackups" :key="backup.id">
            <td>{{ backup.id }}</td>
            <td>{{ formatDate(backup.fecha_creacion) }}</td>
            <td>{{ formatType(backup.tipo) }}</td>
            <td>{{ truncateText(backup.descripcion, 30) }}</td>
            <td>{{ formatSize(backup.tamaño) }}</td>
            <td>{{ truncateText(backup.ubicacion, 20) }}</td>
            <td>{{ backup.creado_por.username }}</td>
            <td class="actions">
              <button class="btn-download" @click="$emit('download', backup.id)">
                <i class="fas fa-download"></i> Descargar
              </button>
              <button class="btn-restore" @click="$emit('restore', backup.id)">
                <i class="fas fa-redo"></i> Restaurar
              </button>
              <button class="btn-delete" @click="$emit('delete', backup.id)">
                <i class="fas fa-trash"></i> Eliminar
              </button>
            </td>
          </tr>
          <tr v-if="filteredBackups.length === 0">
            <td colspan="8" class="no-results">No hay backups disponibles</td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <!-- Pagination would go here -->
  </div>
</template>

<script>
import { ref, computed } from 'vue'

export default {
  props: {
    backups: {
      type: Array,
      default: () => []
    },
    users: {
      type: Array,
      default: () => []
    }
  },
  emits: ['download', 'restore', 'delete'],
  setup(props) {
    // Filters
    const filterType = ref('')
    const filterDate = ref('')
    const filterUser = ref('')
    const truncateText = (value, length) => {
      if (!value) return ''
      value = value.toString()
      return value.length > length ? value.substring(0, length) + '...' : value
    }

    // Formatting functions
    function formatDate(date) {
      return new Date(date).toLocaleString('es-ES', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
    
    function formatType(type) {
      const types = {
        'completo': 'Completo',
        'diferencial': 'Diferencial',
        'incremental': 'Incremental'
      }
      return types[type] || type
    }
    
    function formatSize(bytes) {
      if (bytes === 0) return '0 Bytes'
      const k = 1024
      const sizes = ['Bytes', 'KB', 'MB', 'GB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    }
    
    // Apply filters
    const filteredBackups = computed(() => {
      return props.backups.filter(backup => {
        const matchesType = !filterType.value || backup.tipo === filterType.value
        const matchesUser = !filterUser.value || backup.creado_por.id == filterUser.value
        
        let matchesDate = true
        if (filterDate.value) {
          const backupDate = new Date(backup.fecha_creacion).toISOString().split('T')[0]
          matchesDate = backupDate === filterDate.value
        }
        
        return matchesType && matchesUser && matchesDate
      })
    })
    
    function applyFilters() {
      // Filtering is handled by the computed property
    }
    
    function resetFilters() {
      filterType.value = ''
      filterDate.value = ''
      filterUser.value = ''
    }
    
    return {
      filterType,
      filterDate,
      filterUser,
      filteredBackups,
      truncateText,
      formatDate,
      formatType,
      formatSize,
      applyFilters,
      resetFilters
    }
  }
}
</script>

<style scoped>
.backup-list {
  margin-top: 30px;
}

.backup-list h3 {
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 0 0 20px;
  color: #2E7D32;
  font-size: 16px;
}

.filter-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-bottom: 20px;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 15px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  margin-bottom: 8px;
  font-weight: 500;
  color: #444;
  font-size: 14px;
}

.form-group select, 
.form-group input {
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  transition: border 0.3s;
}

.form-group select:focus, 
.form-group input:focus {
  border-color: #2E7D32;
  outline: none;
  box-shadow: 0 0 0 2px rgba(46, 125, 50, 0.2);
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 10px;
}

.btn-filter, .btn-reset {
  background: white;
  border: 1px solid #ddd;
  padding: 8px 15px;
  border-radius: 5px;
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-filter {
  background: #2E7D32;
  color: white;
  border-color: #2E7D32;
}

.btn-filter:hover {
  background: #1B5E20;
}

.btn-reset:hover {
  background: #f5f5f5;
}

.table-responsive {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

th, td {
  padding: 10px 12px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

th {
  background-color: #f9f9f9;
  font-weight: 600;
  color: #444;
  font-size: 13px;
}

tbody tr:hover {
  background-color: #f5f9f5;
}

.no-results {
  text-align: center;
  padding: 20px;
  color: #777;
}

.actions {
  display: flex;
  gap: 5px;
  flex-wrap: wrap;
}

.btn-download, .btn-restore, .btn-delete {
  padding: 6px 10px;
  border: none;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 5px;
  transition: all 0.2s;
}

.btn-download {
  background: #e3f2ed;
  color: #1e7d34;
}

.btn-restore {
  background: #ffecb3;
  color: #ff8f00;
}

.btn-delete {
  background: #ffebee;
  color: #c62828;
}

.btn-download:hover, .btn-restore:hover, .btn-delete:hover {
  transform: translateY(-1px);
  opacity: 0.9;
}
</style>