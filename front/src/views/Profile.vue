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
              <span v-if="!isEditing">{{ userInfo.city }}, {{ userInfo.country }}</span>
              <div v-else class="flex">
                <InputText v-model="userInfo.city" class="mr-2" placeholder="Город" />
                <InputText v-model="userInfo.country" placeholder="Страна" />
              </div>
            </div>
          </div>
        </div>
        <div>
          <Button v-if="!isEditing" label="Редактировать профиль" icon="pi pi-pencil" @click="editProfile" />
          <Button v-else label="Сохранить" icon="pi pi-check" class="p-button-success mr-2" @click="saveProfile" />
          <Button v-if="isEditing" label="Отмена" icon="pi pi-times" class="p-button-secondary" @click="cancelEdit" />
        </div>
      </div>

      <div class="grid">
        <div class="col-12 md:col-6">
          <Card class="h-full">
            <template #title>Основная информация</template>
            <template #content>
              <div class="grid">
                <div class="col-4 font-bold">Дата рождения:</div>
                <div class="col-8">
                  <InputText v-if="isEditing" v-model="userInfo.dd_mm_yy" type="date" />
                  <span v-else>{{ formattedDate }}</span>
                </div>

                <div class="col-4 font-bold">Email:</div>
                <div class="col-8">
                 
                  <span >{{ user.email }}</span>
                </div>
              </div>
            </template>
          </Card>
        </div>
      </div>

      <!-- Секция "Рекомендуемые курсы" -->
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
import Card from 'primevue/card'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import Tag from 'primevue/tag'
import api from '../utils/api'

const router = useRouter()

const user = ref({})
const userInfo = ref({})
const courses = ref([])
const isEditing = ref(false)
const originalUserInfo = ref({}) // Хранение оригинальных данных на случай отмены

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
    userInfo.value = { ...infoRes.data[0] }
    originalUserInfo.value = { ...infoRes.data[0] } // Сохранение копии данных

    const coursesRes = await api.get('/cources/')
    courses.value = coursesRes.data
  } catch (error) {
    console.error('Ошибка загрузки данных:', error)
  }
}

const editProfile = () => {
  isEditing.value = true
}

const saveProfile = async () => {
  try {
    await api.put(`/form/${userInfo.value.form_id}/`, userInfo.value)
    isEditing.value = false
  } catch (error) {
    console.error('Ошибка при сохранении данных:', error)
  }
}

const cancelEdit = () => {
  userInfo.value = { ...originalUserInfo.value } // Восстановление оригинальных данных
  isEditing.value = false
}

onMounted(loadData)
</script>
