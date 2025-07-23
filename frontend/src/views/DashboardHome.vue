<template>
    <div class="dashboard-home-content">
      <div class="welcome-section">
        <h1 class="text-gradient">Bienvenido, {{ userFullName }}</h1>
        <p>Sistema Integral de Gestión de Activos Tecnológicos</p>
      </div>

      <div class="metrics-container">
        <div class="metric-card glass-card">
          <div class="metric-icon"><i class="fas fa-laptop"></i></div>
          <div class="metric-value">{{ totalDispositivos }}</div>
          <div class="metric-label">Equipos registrados</div>
        </div>
        
        <div class="metric-card glass-card">
          <div class="metric-icon"><i class="fas fa-check-circle"></i></div>
          <div class="metric-value">{{ dispositivosActivos }}</div>
          <div class="metric-label">Equipos en uso</div>
        </div>
        
        <div class="metric-card glass-card">
          <div class="metric-icon"><i class="fas fa-users"></i></div>
          <div class="metric-value">{{ totalUsuarios }}</div>
          <div class="metric-label">Usuarios activos</div>
        </div>
        
        <div class="metric-card glass-card">
          <div class="metric-icon"><i class="fas fa-sync-alt"></i></div>
          <div class="metric-value">{{ ultimaActualizacion }}</div>
          <div class="metric-label">Última actualización</div>
        </div>
      </div>

      <div class="chart-container glass-card">
        <h3>Distribución de equipos</h3>
        <canvas id="equipmentChart"></canvas>
      </div>
    </div>
</template>

<script>
import Chart from 'chart.js/auto';
import DashboardLayout from '@/layouts/Layout.vue';

export default {
  name: 'DashboardHome',
  components: {
    DashboardLayout
  },
  data() {
    return {
      userFullName: '',
      totalDispositivos: 0,
      dispositivosActivos: 0,
      totalUsuarios: 0,
      ultimaActualizacion: '',
      equipmentChart: null
    };
  },
  mounted() {
    this.fetchDashboardData();
  },
  beforeUnmount() {
    if (this.equipmentChart) {
      this.equipmentChart.destroy();
    }
  },
  methods: {
    async fetchDashboardData() {
      try {
        const response = await this.$axios.get('/api/dashboard/');
        const data = response.data;
        
        this.userFullName = data.user_full_name || 'Usuario';
        this.totalDispositivos = data.total_dispositivos;
        this.dispositivosActivos = data.dispositivos_activos;
        this.totalUsuarios = data.total_usuarios;
        this.ultimaActualizacion = this.formatDate(data.ultima_actualizacion);
        
        this.initChart(data.chart_data);
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      }
    },
    formatDate(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      return date.toLocaleDateString('es-ES');
    },
    initChart(chartData) {
      const ctx = document.getElementById('equipmentChart').getContext('2d');
      
      if (this.equipmentChart) {
        this.equipmentChart.destroy();
      }
      
      this.equipmentChart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: chartData.labels,
          datasets: [{
            label: 'Distribución de equipos',
            data: chartData.data,
            backgroundColor: 'rgba(76, 175, 80, 0.6)',
            borderColor: 'rgba(76, 175, 80, 1)',
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              beginAtZero: true,
              grid: {
                color: 'rgba(0, 0, 0, 0.05)'
              }
            },
            x: {
              grid: {
                display: false
              }
            }
          },
          plugins: {
            legend: {
              display: false
            }
          }
        }
      });
    }
  }
};
</script>

<style scoped>
.dashboard-home-content {
  padding: 2rem;
  animation: fadeIn 0.5s ease-out;
}

.welcome-section {
  margin-bottom: 2.5rem;
  text-align: center;
}

.welcome-section h1 {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
  letter-spacing: 0.5px;
}

.welcome-section p {
  font-size: 1.1rem;
  color: var(--primary-black);
  opacity: 0.8;
}

.metrics-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.5rem;
  margin: 2.5rem 0;
}

.metric-card {
  padding: 1.5rem;
  border-radius: 12px;
  text-align: center;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.metric-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0,0,0,0.1);
}

.metric-icon {
  font-size: 2rem;
  color: var(--primary-black);
  margin-bottom: 1rem;
}

.metric-value {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--primary-black);
  margin: 0.5rem 0;
}

.metric-label {
  color: var(--primary-black);
  font-size: 1rem;
  opacity: 0.9;
}

.chart-container {
  padding: 2rem;
  border-radius: 12px;
  margin-top: 2rem;
  position: relative;
}

.chart-container h3 {
  margin-bottom: 1.5rem;
  color: var(--primary-white);
  font-size: 1.3rem;
}

.glass-card {
  background: var(--glass-effect);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: var(--glass-border);
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
  .dashboard-home-content {
    padding: 1.5rem;
  }
  
  .welcome-section h1 {
    font-size: 2rem;
  }
  
  .metrics-container {
    grid-template-columns: 1fr;
  }
}
</style>