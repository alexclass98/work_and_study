<template>
  <div class="surface-ground p-3">
    <div class="surface-card shadow-2 p-3 border-round">
      <div class="flex justify-content-between align-items-center mb-5">
        <div class="flex align-items-center">
          <Avatar :label="userInitials" size="xlarge" class="mr-3" />
          <div>
            <h1 class="text-3xl mb-1">{{ fullName }}</h1>
            <div class="flex align-items-center">
              <i class="pi pi-map-marker mr-2"></i>
              <span>{{ userInfo.city }}, {{ userInfo.country }}</span>
            </div>
          </div>
        </div>
        <Button label="Редактировать профиль" icon="pi pi-pencil" @click="editProfile" />
      </div>

      <div class="grid">
        <div class="col-12 md:col-6">
          <Card class="h-full">
            <template #title>Основная информация</template>
            <template #content>
              <div class="grid">
                <div class="col-4 font-bold">Дата рождения:</div>
                <div class="col-8">{{ formattedDate }}</div>

                <div class="col-4 font-bold">Email:</div>
                <div class="col-8">{{ user.email }}</div>
              </div>
            </template>
          </Card>
        </div>

        <div class="col-12 md:col-6">
          <Card class="h-full">
            <template #title>Навыки</template>
            <template #content>
              <div v-for="skill in skills" :key="skill.id" class="mb-3">
                <div class="flex justify-content-between mb-2">
                  <span>{{ skill.skill_name }}</span>
                  <span>Уровень {{ skill.level }}/10</span>
                </div>
                <ProgressBar :value="skill.level * 10" />
              </div>
            </template>
          </Card>
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
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Avatar from 'primevue/avatar'
import ProgressBar from 'primevue/progressbar'
import Tag from 'primevue/tag'
import Card from 'primevue/card'
import api from '../utils/api'

const router = useRouter()

const user = ref({})
const userInfo = ref({})
const skills = ref([])
const courses = ref([])

const userInitials = computed(() => {
  if (!user.value.first_name || !user.value.last_name) return '??'
  return `${user.value.first_name[0]}${user.value.last_name[0]}`
})

const fullName = computed(() => {
  return `${user.value.username}`
})

const formattedDate = computed(() => {
  return new Date(userInfo.value.dd_mm_yy).toLocaleDateString()
})

const loadData = async () => {
  try {
    const { data } = await api.get('/auth/users/me/')
    user.value = data

    const infoRes = await api.get('/form/')
    userInfo.value = infoRes.data[0]
    console.log(12, infoRes.data[0])

    const skillsRes = await api.get('/user-skill/')
    skills.value = skillsRes.data.map(skill => ({
      ...skill,
      skill_name: skill.skill_id.skill_name
    }))

    const coursesRes = await api.get('/cources/')
    courses.value = coursesRes.data
  } catch (error) {
    console.error('Ошибка загрузки данных:', error)
  }
}

const editProfile = () => {
  router.push('/profile/edit')
}

onMounted(loadData)
</script>