<template>
  <header class="dashboard-header">
    <button 
      class="mobile-menu-toggle" 
      @click="$emit('toggle-sidebar')"
      v-if="isMobile"
    >
      <i class="fas fa-bars"></i>
    </button>

    <div class="logo-container">
      <img :src="logoUrl" alt="Logo" class="logo-img" />
    </div>
    
    <div class="user-info">
      <div class="user-details">
        <div class="user-name">{{ user?.full_name ?? 'Usuario' }}</div>
        <div class="user-role">{{ userRoleDisplay }}</div>
      </div>
      <div class="user-avatar-container" @click="toggleDropdown">
        <div class="user-avatar">
          {{ user.initials || 'US' }}
        </div>
        <div class="user-dropdown" :class="{ show: dropdownOpen }">
          <a href="#" class="dropdown-item" @click.prevent="changePassword">
            <i class="fas fa-lock"></i> Cambiar contraseña
          </a>
          <a href="#" class="dropdown-item" @click.prevent="confirmLogout">
            <i class="fas fa-sign-out-alt"></i> Cerrar sesión
          </a>
        </div>
      </div>
    </div>
  </header>
</template>

<script>
export default {
  name: 'AppHeader',
  props: {
    user: {
      type: Object,
      default: () => ({ full_name: 'Invitado', role: 'guest'}),
      required: true
    },
    isMobile: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      dropdownOpen: false,
      logoUrl: '/static/images/logo-institucion.png'
    }
  },
  computed: {
    userRoleDisplay() {
      const roles = {
        'superadmin': 'Super Administrador',
        'admin': 'Administrador',
        'guest': 'Invitado'
      }
      return roles[this.user.role] || 'Invitado'
    }
  },
  methods: {
    toggleDropdown() {
      this.dropdownOpen = !this.dropdownOpen
    },
    changePassword() {
      this.$router.push('/password-change')
      this.dropdownOpen = false
    },
    confirmLogout() {
      this.dropdownOpen = false
      this.$emit('logout')
    }
  }
}
</script>

<style scoped>
/* Estilos específicos del header que complementan dashboard.css */
.user-dropdown {
  position: absolute;
  right: 0;
  top: 60px;
  background-color: var(--primary-white);
  border-radius: 8px;
  box-shadow: 0 8px 20px rgba(0,0,0,0.1);
  width: 220px;
  overflow: hidden;
  z-index: 20;
  opacity: 0;
  visibility: hidden;
  transform: translateY(-10px);
  transition: all 0.3s ease;
}

.user-dropdown.show {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  color: var(--primary-black);
  text-decoration: none;
  transition: all 0.2s ease;
}

.dropdown-item:hover {
  background-color: var(--secondary-gray);
  color: var(--primary-green);
}

.dropdown-item i {
  width: 20px;
  text-align: center;
}

@media (max-width: 768px) {
  .user-details {
    display: none;
  }
  
  .dashboard-header {
    padding: 0 1rem;
  }
}
</style>