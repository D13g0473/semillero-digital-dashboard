<template>
  <q-table
    title="Progreso de Alumnos"
    :rows="students"
    :columns="columns"
    row-key="id"
    :loading="loading"
  >
    <template v-slot:body-cell-progress="props">
      <q-td :props="props">
        <q-linear-progress :value="calculateProgress(props.row.metrics)" color="primary" style="height: 20px">
          <div class="absolute-full flex flex-center">
            <span class="text-white">{{ Math.round(calculateProgress(props.row.metrics) * 100) }}%</span>
          </div>
        </q-linear-progress>
      </q-td>
    </template>
  </q-table>
</template>

<script setup>
import { ref } from 'vue';

defineProps({
  students: {
    type: Array,
    required: true,
  },
  loading: {
    type: Boolean,
    default: false,
  },
});

const columns = ref([
  { name: 'fullName', label: 'Alumno', field: 'fullName', align: 'left', sortable: true },
  { name: 'email', label: 'Email', field: 'email', align: 'left', sortable: true },
  {
    name: 'progress',
    label: 'Progreso de Entregas',
    align: 'center',
    sortable: false,
  },
  { name: 'on_time', label: 'A Tiempo', field: row => row.metrics.on_time, align: 'center', sortable: true },
  { name: 'late', label: 'Tarde', field: row => row.metrics.late, align: 'center', sortable: true },
  { name: 'graded', label: 'Calificadas', field: row => row.metrics.graded, align: 'center', sortable: true },
  { name: 'missing', label: 'Faltantes', field: row => row.metrics.missing, align: 'center', sortable: true },
  { name: 'total', label: 'Total Tareas', field: row => row.metrics.total_assignments, align: 'center', sortable: true },
]);

const calculateProgress = (metrics) => {
  if (!metrics || metrics.total_assignments === 0) {
    return 0;
  }
  const completed = (metrics.on_time || 0) + (metrics.late || 0) + (metrics.graded || 0);
  return completed / metrics.total_assignments;
};

</script>
