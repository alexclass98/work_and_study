<template>
  <div class="surface-ground min-h-screen p-3">
    <div class="surface-card shadow-2 p-3 border-round">
      <div class="flex justify-content-between mb-3">
        <h1 class="text-3xl text-primary">Добро пожаловать! {{ user.username }}</h1>
        <Button v-if="!user.value" label="Войти" @click="logout" />
        <Button v-else label="Выйти" @click="logout" />
      </div>
    </div>
    
      <Card class="mt-3">
        <template #title>Рекомендуемые курсы</template>
        <template #content>
          <div class="grid">
            <div v-for="course in courses" :key="course.id" class="col-12 md:col-4">
              <div class="border-round surface-section shadow-2 p-3">
                <h3 class="text-xl mb-2">{{ course.name }}</h3>
                <div class="flex justify-content-between mb-3">
                  <Tag :value="'Сложность: ' + course.difficulty" />
                  <Tag :value="course.duration_hrs + ' часов'" icon="pi pi-clock" />
                </div>
                <p class="line-height-3">{{ course.description }}</p>
                <Button label="Подробнее" class="mt-3" />
              </div>
            </div>
          </div>
        </template>
      </Card>
   
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../utils/api'

const router = useRouter()
const user = ref({})

const courses = ref([])

const logout = () => {
  localStorage.removeItem('accessToken')
  router.push('/auth')
}

onMounted(async () => {
  try {
    const { data } = await api.get('/auth/users/me/')
    user.value = data
    const coursesRes = await api.get('/cources/')
    courses.value = coursesRes.data
    console.log(courses.value)
  } catch (error) {
    console.error('Data fetching error:', error)
  }
  
})
</script>