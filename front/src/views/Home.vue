<template>
  <div class="surface-ground min-h-screen p-3">
    <div class="surface-card shadow-2 p-3 border-round">
      <div class="flex justify-content-between mb-3">
        <h1 class="text-3xl text-primary">Добро пожаловать, {{ user.username }}!</h1>
        <Button label="Выйти" @click="logout" />
      </div>

      <div class="grid">
        <div class="col-12 md:col-4">
          <Card class="h-full">
            <template #title>Ваши навыки</template>
            <template #content>
              <div v-for="skill in skills" :key="skill.id">
                {{ skill.skill_name }} - Уровень {{ skill.level }}
              </div>
            </template>
          </Card>
        </div>

        <div class="col-12 md:col-8">
          <Card class="h-full">
            <template #title>Рекомендуемые курсы</template>
            <template #content>
              <DataTable :value="courses">
                <Column field="name" header="Название"></Column>
                <Column field="difficulty" header="Сложность"></Column>
                <Column field="duration_hrs" header="Длительность (часы)"></Column>
              </DataTable>
            </template>
          </Card>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../utils/api'

const router = useRouter()
const user = ref({})
const skills = ref([])
const courses = ref([])

const logout = () => {
  localStorage.removeItem('accessToken')
  router.push('/auth')
}

onMounted(async () => {
  try {
    const { data } = await api.get('/auth/users/me/')
    user.value = data

    const skillsRes = await api.get('/user-skill/')
    skills.value = skillsRes.data

    const coursesRes = await api.get('/cources/')
    courses.value = coursesRes.data
  } catch (error) {
    console.error('Data fetching error:', error)
  }
})
</script>