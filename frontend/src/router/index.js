import { createRouter, createWebHistory } from 'vue-router';
import MainLayout from '../layouts/MainLayout.vue';
import Dashboard from '../pages/Dashboard.vue';
import Profesor from '../pages/Profesor.vue';
import Alumno from '../pages/Alumno.vue';

const routes = [
  {
    path: '/',
    component: MainLayout,
    children: [
      {
        path: '',
        name: 'Dashboard',
        component: Dashboard
      },
      {
        path: 'profesor',
        name: 'Profesor',
        component: Profesor
      },
      {
        path: 'alumno',
        name: 'Alumno',
        component: Alumno
      }
    ]
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
