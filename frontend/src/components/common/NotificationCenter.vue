<template>
  <div class="notification-container">
    <transition-group name="notification" tag="div">
      <div 
        v-for="notification in notifications"
        :key="notification.id"
        class="notification"
        :class="`notification-${notification.type}`"
        @click="removeNotification(notification.id)"
      >
        <div class="notification-icon">
          <i :class="iconMap[notification.type]"></i>
        </div>
        <div class="notification-content">
          <h4 class="notification-title">{{ notification.title }}</h4>
          <p class="notification-message">{{ notification.message }}</p>
        </div>
        <button class="notification-close" @click.stop="removeNotification(notification.id)">
          <i class="fas fa-times"></i>
        </button>
      </div>
    </transition-group>
  </div>
</template>

<script>

import { mapState } from 'vuex';

export default {
  name: 'NotificationCenter',
  data() {
    return {
      iconMap: {
        success: 'fas fa-check-circle',
        error: 'fas fa-exclamation-circle',
        warning: 'fas fa-exclamation-triangle',
        info: 'fas fa-info-circle'
      }
    }
  },
  computed: {
    ...mapState('notifications', ['list']),
    notifications() {
      return this.list || [];
    }
  },
  methods: {
    async removeNotification(id) {
      try {
        await this.$store.dispatch('notifications/remove', id);
      } catch (error) {
        console.error('Error removing notification:', error);
      }
    }
  }
}
</script>

<style scoped>
.notification-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 9999;
  max-width: 350px;
  width: 100%;
}

.notification {
  display: flex;
  align-items: flex-start;
  padding: 15px;
  margin-bottom: 15px;
  border-radius: 8px;
  background-color: white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.notification::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
}

.notification-success {
  border-left: 4px solid #2E7D32;
}

.notification-success .notification-icon {
  color: #2E7D32;
}

.notification-error {
  border-left: 4px solid #d32f2f;
}

.notification-error .notification-icon {
  color: #d32f2f;
}

.notification-warning {
  border-left: 4px solid #ffa000;
}

.notification-warning .notification-icon {
  color: #ffa000;
}

.notification-info {
  border-left: 4px solid #1976d2;
}

.notification-info .notification-icon {
  color: #1976d2;
}

.notification-icon {
  font-size: 1.5rem;
  margin-right: 15px;
  flex-shrink: 0;
}

.notification-content {
  flex-grow: 1;
}

.notification-title {
  margin: 0 0 5px 0;
  font-size: 1rem;
  font-weight: 600;
  color: #212121;
}

.notification-message {
  margin: 0;
  font-size: 0.9rem;
  color: #424242;
}

.notification-close {
  background: none;
  border: none;
  color: #757575;
  cursor: pointer;
  margin-left: 10px;
  padding: 0;
  font-size: 1rem;
  transition: color 0.2s;
}

.notification-close:hover {
  color: #212121;
}

/* Animaciones */
.notification-enter-active,
.notification-leave-active {
  transition: all 0.5s ease;
}

.notification-enter-from,
.notification-leave-to {
  opacity: 0;
  transform: translateX(100%);
}

.notification-move {
  transition: transform 0.5s ease;
}
</style>