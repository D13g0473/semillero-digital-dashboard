<template>
  <q-page padding>
    <div v-if="loading" class="text-center">
      <q-spinner-dots color="primary" size="40px" />
      <p>Cargando cursos...</p>
    </div>

    <div v-else-if="error" class="q-pa-md bg-red-1 text-red-8">
      <p class="text-weight-bold">Ocurrió un error:</p>
      <p>{{ error }}</p>
      <q-btn label="Iniciar Sesión" color="primary" href="http://localhost:5001/login" />
    </div>

    <div v-else>
      <q-table
        title="Mis Cursos"
        :rows="courses"
        :columns="columns"
        row-key="id"
      />
    </div>
  </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { api } from '../boot/axios';

const courses = ref([]);
const loading = ref(true);
const error = ref(null);

const columns = [
  { name: 'name', required: true, label: 'Nombre del Curso', align: 'left', field: 'name', sortable: true },
  { name: 'section', label: 'Sección', align: 'left', field: 'section', sortable: true },
  { name: 'owner', label: 'ID del Propietario', align: 'left', field: 'ownerId' },
  { name: 'status', label: 'Estado', align: 'left', field: 'courseState' },
];

onMounted(async () => {
  try {
    const response = await api.get('/courses');
    courses.value = response.data;
  } catch (err) {
    if (err.response && err.response.status === 401) {
      error.value = 'No estás autenticado. Por favor, inicia sesión.';
    } else {
      error.value = err.message || 'No se pudo conectar con el servidor.';
    }
    console.error(err);
  } finally {
    loading.value = false;
  }
});
</script>
