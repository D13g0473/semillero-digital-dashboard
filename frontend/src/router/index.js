import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../pages/Dashboard.vue'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard
  },
  // Aquí se pueden añadir más rutas en el futuro
  // {
  //   path: '/profesor/:id',
  //   name: 'Profesor',
  //   component: () => import('../pages/Profesor.vue')
  // }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
