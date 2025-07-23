import { createRouter, createWebHistory } from 'vue-router'
import Login from '@/views/Login.vue'
import DashboardHome from '@/views/DashboardHome.vue'
import DashboardLayout from '../layouts/Layout.vue'

const routes = [
  {
    path: '/',
    redirect: '/login' // Redirige la raíz al login
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/dashboard',
    component: DashboardLayout,
    meta: { requiresAuth: true }, // Protege esta ruta
    children: [
      {
        path: '',
        name: 'DashboardHome',
        component: () => import ('@/views/DashboardHome.vue'),
      },
      {
        path: 'inventario',
        name: 'Inventario',
        component: () => import ('@/views/Inventario.vue'),
        meta: {
          navKey: 'inventario'
        }
      },
      {
        path: 'usuarios',
        name: 'Usuarios',
        component: () => import ('@/views/Usuarios.vue'),
        meta: {
          navKey: 'usuarios'
        }
      },
      {
        path: 'mantenimiento',
        name: 'Mantenimiento',
        component: () => import ('@/views/Mantenimiento.vue'),
        meta: {
          navKey: 'mantenimiento'
        }
      },
      {
        path: 'reportes',
        name: 'Reportes',
        component: () => import ('@/views/Reportes.vue'),
        meta: {
          navKey: 'reportes'
        }
      },
      {
        path: 'backups',
        name: 'Backup',
        component: () => import ('@/components/backups/Backups.vue'),
        meta: {
          navKey: 'backups'
        }
      },
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  // Función mejorada para verificar cookies
  function checkAuth() {
    return document.cookie.split(';').some(cookie => {
      return cookie.trim().startsWith('csrftoken');
    });
  }

  const isAuthenticated = checkAuth();

  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!isAuthenticated) {
      next('/login');
    } else {
      // Verificar si es usuario invitado
      const isGuest = document.cookie.split(';').some(cookie => {
        return cookie.trim().startsWith('user_role=invitado');
      });

      // Rutas permitidas para invitados
      const guestAllowedRoutes = ['DashboardHome', 'Reportes'];
      
      if (isGuest && !guestAllowedRoutes.includes(to.name)) {
        next('/dashboard'); // Redirigir al home del dashboard
      } else {
        if (to.path === '/login') {
          next('/dashboard'); // Redirige si ya está autenticado
        } else {
          next(); // Permite acceso a la ruta protegida
        }
      }
    }
  } else {
    next(); // Rutas públicas
  }
});
export default router