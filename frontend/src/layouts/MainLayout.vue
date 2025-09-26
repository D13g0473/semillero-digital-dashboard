<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="toggleLeftDrawer"
        />

        <q-toolbar-title>
          Semillero Digital Dashboard
        </q-toolbar-title>

        <div>v0.1</div>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
    >
      <q-list>
        <q-item-label
          header
        >
          Menú de Navegación
        </q-item-label>

        <EssentialLink
          v-for="link in essentialLinks"
          :key="link.title"
          v-bind="link"
        />
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { ref } from 'vue'
import EssentialLink from '../components/EssentialLink.vue'

const essentialLinks = [
  {
    title: 'Dashboard General',
    caption: 'Vista de todos los cursos',
    icon: 'dashboard',
    link: '/'
  },
  {
    title: 'Vista Profesor',
    caption: 'Métricas de tus cursos',
    icon: 'school',
    link: '/profesor'
  },
    {
    title: 'Vista Alumno',
    caption: 'Progreso del alumno',
    icon: 'face',
    link: '/alumno'
  },
];

const leftDrawerOpen = ref(false)

function toggleLeftDrawer() {
  leftDrawerOpen.value = !leftDrawerOpen.value
}
</script>
