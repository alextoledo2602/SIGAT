<template>
  <div class="report-results">
    <div class="results-header">
      <h3>Resultados del Reporte</h3>
      <div class="export-options">
        <button class="btn-export pdf" @click="$emit('export', 'pdf')">
          <i class="fas fa-file-pdf"></i> Exportar a PDF
        </button>
        <button class="btn-export excel" @click="$emit('export', 'excel')">
          <i class="fas fa-file-excel"></i> Exportar a Excel
        </button>
      </div>
    </div>
    
    <div class="results-table">
      <table>
        <thead>
          <tr>
            <th>N° Inventario</th>
            <th>Tipo</th>
            <th>Marca</th>
            <th>Modelo</th>
            <th>Serial</th>
            <th>Ubicación</th>
            <th>Estado</th>
            <th>Responsable</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="devices.length > 0" v-for="device in devices" :key="device.numero_inventario">
            <td>{{ device.numero_inventario }}</td>
            <td>{{ device.tipo }}</td>
            <td>{{ device.marca }}</td>
            <td>{{ device.modelo }}</td>
            <td>{{ device.serial }}</td>
            <td>{{ device.ubicacion }}</td>
            <td>{{ device.estado }}</td>
            <td>{{ device.responsable }}</td>
          </tr>
          <tr v-else>
            <td colspan="8" class="no-results">
              {{ hasResults ? 'No se encontraron dispositivos con los filtros seleccionados.' : 'Seleccione filtros y genere un reporte.' }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    devices: {
      type: Array,
      default: () => []
    },
    hasResults: {
      type: Boolean,
      default: false
    }
  },
  emits: ['export']
}
</script>

<style scoped>
.report-results {
  border: 1px solid #eee;
  border-radius: 8px;
  overflow: hidden;
}

.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 15px;
  background: #f9f9f9;
  border-bottom: 1px solid #eee;
}

.results-header h3 {
  font-size: 16px;
  margin: 0;
  color: #333;
}

.export-options {
  display: flex;
  gap: 8px;
}

.btn-export {
  background: white;
  border: 1px solid #ddd;
  padding: 6px 12px;
  border-radius: 5px;
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-export:hover {
  background: #f5f5f5;
  transform: translateY(-1px);
}

.btn-export.pdf {
  color: #e53935;
  border-color: #e53935;
}

.btn-export.excel {
  color: #1e7d34;
  border-color: #1e7d34;
}

.results-table {
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
  font-size: 14px;
}
</style>