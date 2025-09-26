<template>
  <q-page class="q-pa-md">
    <div v-if="loading" class="flex flex-center">
      <q-spinner-dots color="primary" size="40px" />
      <p class="q-ml-md">Cargando datos del profesor...</p>
    </div>

    <div v-else-if="error">
      <q-banner inline-actions class="text-white bg-red">
        <template v-slot:avatar>
          <q-icon name="error" />
        </template>
        {{ error }}
      </q-banner>
    </div>

    <div v-else>
      <div class="row items-center q-mb-md">
        <div class="col-md-6 col-12">
            <q-select
                v-model="selectedCourse"
                :options="courses"
                option-value="id"
                option-label="name"
                label="Selecciona un curso"
                emit-value
                map-options
                outlined
                />
        </div>
      </div>

      <div v-if="currentCourseData">
        <div class="row q-col-gutter-md">
          <div class="col-12 col-md-5">
            <q-card class="my-card">
              <q-card-section>
                 <CourseOverviewChart :students="currentCourseData.students" />
              </q-card-section>
            </q-card>
          </div>
          <div class="col-12 col-md-7">
             <q-card class="my-card">
              <q-card-section>
                <div class="text-h6">{{ currentCourseData.name }}</div>
                <div class="text-subtitle2">{{ currentCourseData.description }}</div>
              </q-card-section>
            </q-card>
          </div>
        </div>

        <q-separator class="q-my-lg" />

        <ProgressTable :students="currentCourseData.students" :loading="loading" />

      </div>
       <div v-else class="flex flex-center q-mt-xl">
          <q-icon name="school" size="xl" color="grey-5" />
          <p class="text-h6 text-grey-5 q-ml-md">Selecciona un curso para ver las métricas.</p>
      </div>
    </div>
  </q-page>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios'; // Asegúrate de que boot/axios.js esté configurado
import CourseOverviewChart from '../components/CourseOverviewChart.vue';
import ProgressTable from '../components/ProgressTable.vue';

const courses = ref([]);
const selectedCourse = ref(null);
const loading = ref(true);
const error = ref(null);

const fetchTeacherDashboard = async () => {
  try {
    // Usamos la instancia de axios configurada para incluir credenciales
    const response = await axios.get('/api/teacher/dashboard');
    courses.value = response.data;
    if (courses.value.length > 0) {
      // Seleccionar el primer curso por defecto
      selectedCourse.value = courses.value[0].id;
    }
  } catch (err) {
    console.error('Error fetching teacher dashboard:', err);
    error.value = 'No se pudieron cargar los datos. Asegúrate de haber iniciado sesión.';
  } finally {
    loading.value = false;
  }
};

const currentCourseData = computed(() => {
  if (!selectedCourse.value || courses.value.length === 0) {
    return null;
  }
  return courses.value.find(c => c.id === selectedCourse.value);
});

onMounted(() => {
  fetchTeacherDashboard();
});

</script>
