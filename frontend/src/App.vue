<template>
  <div id="app">
    <!-- Componente de notificaciones globales -->
    <notification-center />
    
    <!-- Router view envuelto en tu layout -->
    <dashboard-layout v-if="userAuthenticated" :user="currentUser">
      <router-view />
    </dashboard-layout>
    
    <!-- Páginas de autenticación sin layout -->
    <router-view v-else />
    
    <!-- Modal global -->
     <!-- <modal-confirm />-->
    
  </div>
</template>

<script>
import DashboardLayout from '@/layouts/Layout.vue'
import NotificationCenter from '@/components/common/NotificationCenter.vue'
import ModalConfirm from '@/components/common/ModalConfirm.vue'

export default {
  name: 'App',
  components: {
    DashboardLayout,
    NotificationCenter,
    ModalConfirm
  },
  computed: {
    userAuthenticated() {
      return this.$store.state.auth.authenticated
    },
    currentUser() {
      return this.$store.state.auth.user
    }
  },
  created() {
    // Inicializar datos del usuario desde Django
    if (window.userData) {
      this.$store.dispatch('auth/setUser', window.userData)
    }
  }
}
</script>
<style>
body, #app {
  min-height: 100vh;
  background-image: url('@/assets/images/background.png');
  background-size: cover;
  background-position: center;
  background-attachment: fixed; /* Efecto fijo/parallax */
  background-repeat: no-repeat;
  margin: 0;
}
</style>