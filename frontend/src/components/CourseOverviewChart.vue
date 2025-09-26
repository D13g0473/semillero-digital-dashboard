<template>
  <div class="chart-container">
    <Doughnut v-if="chartData.datasets.length > 0" :data="chartData" :options="chartOptions" />
    <p v-else>No hay datos de entregas para mostrar.</p>
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue';
import { Doughnut } from 'vue-chartjs';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  CategoryScale,
} from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, ArcElement, CategoryScale);

const props = defineProps({
  students: {
    type: Array,
    required: true,
    default: () => [],
  },
});

const chartData = ref({ labels: [], datasets: [] });

const chartOptions = ref({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'top',
    },
    title: {
      display: true,
      text: 'Estado General de Entregas del Curso',
    },
  },
});

// Lógica para procesar los datos de los alumnos y actualizar el gráfico
const aggregatedMetrics = computed(() => {
  const totals = {
    on_time: 0,
    late: 0,
    missing: 0,
    graded: 0,
  };

  props.students.forEach(student => {
    totals.on_time += student.metrics.on_time || 0;
    totals.late += student.metrics.late || 0;
    totals.missing += student.metrics.missing || 0;
    totals.graded += student.metrics.graded || 0;
  });

  return totals;
});

watch(aggregatedMetrics, (newMetrics) => {
  if (props.students.length > 0) {
    const totalSubmissions = newMetrics.on_time + newMetrics.late + newMetrics.missing + newMetrics.graded;
    if (totalSubmissions > 0) {
        chartData.value = {
        labels: ['Entregado a Tiempo', 'Entregado Tarde', 'Calificado', 'Faltante'],
        datasets: [
          {
            backgroundColor: ['#4CAF50', '#FFC107', '#2196F3', '#F44336'],
            data: [newMetrics.on_time, newMetrics.late, newMetrics.graded, newMetrics.missing],
          },
        ],
      };
    } else {
        chartData.value = { labels: [], datasets: [] };
    }
  } else {
    chartData.value = { labels: [], datasets: [] };
  }
}, { immediate: true });

</script>

<style scoped>
.chart-container {
  position: relative;
  height: 40vh;
  width: 100%;
}
</style>
