<template>
  <div class="dashboard">
    <AppHeader 
      :user="user"
      @toggle-sidebar="toggleSidebar"
      @logout="handleLogout"
      class="dashboard-header"
    />
    
    <AppSidebar
      :sidebar-open="sidebarOpen"
      :is-mobile="isMobile"
      :active-tab="activeTab"
      @close-sidebar="sidebarOpen = false"
      class="dashboard-nav"
      :class="{ active: sidebarOpen }"
    />
    
    <main class="dashboard-main">
      <div class="scrollable-container">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </div>
    </main>
    
    
  </div>
</template>

<script>
import AppHeader from '@/components/layout/AppHeader.vue'
import AppSidebar from '@/components/layout/AppSidebar.vue'

export default {
  name: 'DashboardLayout',
  components: {
    AppHeader,
    AppSidebar
  },
  props: {
    activeTab: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      isMobile: false,
      sidebarOpen: true,
      currentYear: new Date().getFullYear(),
      user: {
        full_name: 'Nombre Usuario',
        role: 'admin',
        initials: 'NU'
      }
    }
  },
  mounted() {
    this.checkMobile()
    window.addEventListener('resize', this.checkMobile)
    this.fetchUserData()
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.checkMobile)
  },
  methods: {
    checkMobile() {
      this.isMobile = window.innerWidth < 992
      if (!this.isMobile) {
        this.sidebarOpen = true
      } else {
        this.sidebarOpen = false
      }
    },
    toggleSidebar() {
      this.sidebarOpen = !this.sidebarOpen
    },
    async fetchUserData() {
      try {
        const response = await this.$axios.get('/api/user/profile/')
        if (response.data) {
          this.user = {
            ...response.data,
            initials: this.getInitials(response.data.full_name)
          }
        }
      } catch (error) {
        console.error('Error fetching user data:', error)
      }
    },
    getInitials(name) {
      if (!name) return 'US'
      const parts = name.split(' ')
      return parts.length > 1 
        ? `${parts[0][0]}${parts[parts.length-1][0]}`.toUpperCase()
        : name.substring(0, 2).toUpperCase()
    },
    handleLogout() {
      this.$store.dispatch('logout')
      this.$router.push('/login')
    }
  }
}
</script>

<style>
@import '@/assets/dashboard.css';

/* Añadidos específicos para la integración */
.dashboard-main{
  background-color: transparent;
}
.dashboard-nav.active {
  left: 0;
}

/* Ajustes para el contenido principal */
.scrollable-container {
  padding-bottom: 80px; /* Espacio para el footer */
}

/* Responsive adjustments */
@media (max-width: 992px) {
  .dashboard-footer {
    left: 0;
  }
  
  .dashboard-main {
    margin-left: 0;
    margin-top: 80px;
    padding: 1.5rem;
  }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>