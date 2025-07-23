<template>
  <div class="reports-container">
    <div class="card">
      <h2><i class="fas fa-file-alt"></i> Generar Reportes</h2>
      
      <form @submit.prevent="generateReport" class="filter-form">
        <div class="form-row">
          <div class="form-group">
            <label for="report-type">Tipo de Reporte:</label>
            <select id="report-type" v-model="reportType" required>
              <option value="">-- Seleccionar tipo --</option>
              <option value="equipos">Reporte de Equipos</option>
              <option value="usuarios">Reporte de Usuarios</option>
              <option value="asignaciones">Reporte de Asignaciones</option>
              <option value="mantenimientos">Reporte de Mantenimientos</option>
              <option value="completo">Reporte Completo</option>
            </select>
          </div>
          
          <div class="form-group">
            <label for="fecha-inicio">Fecha Inicio:</label>
            <input type="date" id="fecha-inicio" v-model="startDate">
          </div>
          
          <div class="form-group">
            <label for="fecha-fin">Fecha Fin:</label>
            <input type="date" id="fecha-fin" v-model="endDate">
          </div>
        </div>
        
        <div class="form-row">
          <div class="form-group">
            <label for="estado">Estado del Equipo:</label>
            <select id="estado" v-model="status">
              <option value="">Todos los estados</option>
              <option value="Activo">Activo</option>
              <option value="En reparación">En reparación</option>
              <option value="Baja">Baja</option>
            </select>
          </div>
          
          <div class="form-group">
            <label for="ubicacion">Ubicación:</label>
            <select id="ubicacion" v-model="location">
              <option value="">Todas las ubicaciones</option>
              <option value="Departamento de Sistema">Departamento de Sistema</option>
              <option value="Gerencia Financiera">Gerencia Financiera</option>
              <option value="Seguridad y Protección">Seguridad y Protección</option>
              <option value="Atención al hombre">Atención al hombre</option>
              <option value="Auditoría">Auditoría</option>
            </select>
          </div>
          
          <div class="form-group">
            <label for="usuario">Usuario:</label>
            <select id="usuario" v-model="user">
              <option value="">Todos los usuarios</option>
              <option v-for="user in users" :key="user.id" :value="user.id">
                {{ user.username }}
              </option>
            </select>
          </div>
        </div>
        
        <div class="form-actions">
          <button type="submit" class="btn-generate">
            <i class="fas fa-cogs"></i> Generar Reporte
          </button>
        </div>
      </form>
      
      <ReportsTable 
        :devices="devices" 
        :hasResults="hasResults"
        @export="handleExport"
      />
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import ReportsTable from '@/components/reports/ReportsTable.vue'


export default {
  components: {
    ReportsTable
  },
  setup() {
    
    
    // Form data
    const reportType = ref('')
    const startDate = ref('')
    const endDate = ref('')
    const status = ref('')
    const location = ref('')
    const user = ref('')
    
    // Mock data - in a real app this would come from an API
    const users = ref([
      { id: 1, username: 'admin' },
      { id: 2, username: 'user1' },
      { id: 3, username: 'user2' }
    ])
    
    const devices = ref([])
    const hasResults = computed(() => devices.value.length > 0)
    
    function generateReport() {
      // Simulate API call
      setTimeout(() => {
        // Mock data
        devices.value = [
          {
            numero_inventario: 'INV001',
            tipo: 'Laptop',
            marca: 'Dell',
            modelo: 'XPS 15',
            serial: 'SN123456',
            ubicacion: 'Departamento de Sistema',
            estado: 'Activo',
            responsable: 'admin'
          },
          {
            numero_inventario: 'INV002',
            tipo: 'Monitor',
            marca: 'HP',
            modelo: '24f',
            serial: 'SN789012',
            ubicacion: 'Gerencia Financiera',
            estado: 'Activo',
            responsable: 'user1'
          }
        ]
        
        
      }, 500)
    }
    
    function handleExport(format) {
      if (!hasResults.value) {
        toast.error('No hay datos para exportar')
        return
      }
      
      toast.info(`Generando ${format.toUpperCase()}...`)
      // In a real app, this would trigger a download
    }
    
    return {
      reportType,
      startDate,
      endDate,
      status,
      location,
      user,
      users,
      devices,
      hasResults,
      generateReport,
      handleExport
    }
  }
}
</script>

<style scoped>
.reports-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
}

.card {
  background: white;
  border-radius: 10px;
  padding: 25px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
}

.card h2 {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
  color: #2E7D32;
}

.filter-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-bottom: 30px;
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
  margin-top: 10px;
}

.btn-generate {
  background: linear-gradient(135deg, #2E7D32, #1B5E20);
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s;
  font-size: 14px;
}

.btn-generate:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(46, 125, 50, 0.3);
}
</style>