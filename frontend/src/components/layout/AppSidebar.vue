<template>
  <nav 
    class="dashboard-nav" 
    :class="{ active: sidebarOpen }"
    @click.stop
  >
    <ul class="nav-menu">
      <li 
        v-for="item in menuItems" 
        :key="item.path" 
        class="nav-item"
      >
        <router-link 
          :to="item.path" 
          class="nav-link"
          :class="{ active: isActive(item) }"
        >
          <i :class="item.icon"></i>
          <span>{{ item.label }}</span>
        </router-link>
      </li>

      <li class="nav-item-logo">
        <div class="logo-sigat-container">
          <img 
            src="@/assets/images/sigat2-transparent.png" 
            alt="Logo SIGAT" 
            class="logo-sigat-img" 
          />
        </div>
      </li>
      <li class="nav-footer">
        <div class="footer-content">
          <p> &copy; {{ currentYear }} </p>
          <div class="version">v1.0.0</div>
        </div>
      </li>
    </ul>
  </nav>
</template>

<script>
export default {
  name: 'AppSidebar',
  props: {
    sidebarOpen: {
      type: Boolean,
      default: false
    },
    isMobile: {
      type: Boolean,
      default: false
    },
    activeTab: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      currentYear: new Date().getFullYear(),
      menuItems: [
        {
          path: '/dashboard',
          label: 'Inicio',
          icon: 'fas fa-home',
          navKey: 'home'
        },
        {
          path: '/dashboard/inventario',
          label: 'Inventario',
          icon: 'fas fa-boxes',
          navKey: 'inventario'
        },
        {
          path: '/dashboard/usuarios',
          label: 'Usuarios',
          icon: 'fas fa-users',
          navKey: 'usuarios'
        },
        {
          path: '/dashboard/mantenimiento',
          label: 'Mantenimiento',
          icon: 'fas fa-tools',
          navKey: 'mantenimiento'
        },
        {
          path: '/dashboard/reportes',
          label: 'Reportes',
          icon: 'fas fa-chart-bar',
          navKey: 'reportes'
        },
        {
          path: '/dashboard/backups',
          label: 'Respaldo',
          navKey: 'backups'
        }
      ]
    }
  },
  methods: {
    isActive(item) {
  // Prioriza la comparación por navKey si está disponible
  if (this.activeTab) {
    return item.navKey === this.activeTab
  }
  
  // Comparación exacta de rutas
  if (this.$route.path === item.path) {
    return true
  }
  
  // Caso especial para la ruta home (/dashboard)
  if (item.navKey === 'home') {
    return this.$route.path === '/dashboard' || 
           this.$route.path === '/dashboard/'
  }
  
  return false
}
  },
  watch: {
    '$route'() {
      if (this.isMobile) {
        this.$emit('close-sidebar')
      }
    }
  }
}
</script>

<style scoped>
/* Estilos específicos del sidebar que complementan dashboard.css */
.logo-sigat-container {
  display: flex;
  align-items: center;
  justify-content: center; /* Centra horizontalmente */
  padding: 20px 0; /* Espaciado vertical */
  margin-top: auto; /* Lo empuja hacia abajo */
  text-align: center;
  border-top: 1px solid #eee; /* Opcional: línea separadora */
}

.logo-sigat-img {
  max-width: 100%;
  max-height: 55px;
  opacity: 0.9;
  transition: opacity 0.3s ease;
}

.logo-sigat-img:hover {
  opacity: 1;
}

.nav-item-logo {
  margin-top: auto;
  padding-bottom: 1rem;
}

/* Ajustes para íconos */
.nav-link i {
  width: 24px;
  text-align: center;
  font-size: 1.1rem;
}

/* Efecto de hover más suave */
.nav-link:hover {
  transform: translateX(5px) scale(1.02);
}
.nav-footer {
  display: flex;
  align-items: center;  
  padding: 0.5rem 4rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.footer-content {
  display: flex;
  flex-direction: row;
  text-align: center;
  color: var(--primary-white);
  opacity: 0.7;
  font-size: 0.85rem;
}

.footer-content p {
  margin-bottom: 0.5rem;
}

.version {
  padding-left: 1rem;
  font-size: 0.75rem;
  opacity: 0.6;
}

/* Ajustes para mobile */
@media (max-width: 992px) {
  .dashboard-nav {
    box-shadow: 4px 0 15px rgba(0,0,0,0.1);
  }
  
  .logo-sigat-container {
    padding: 0.5rem;
  }
}
</style>