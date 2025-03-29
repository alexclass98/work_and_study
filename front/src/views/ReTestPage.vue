<template>
  <div class="p-4 surface-card shadow-2 border-round">
    <h1 class="text-3xl font-bold mb-3">{{ skill.skill_name }}</h1>
    
    <div class="flex align-items-center gap-2 mb-3">
      <Tag 
        :value="skill.type === true ? 'Hard' : 'Soft'" 
        :severity="skill.type === true ? 'primary' : 'success'" 
        :icon="skill.type === true ? 'pi pi-cog' : 'pi pi-user'" 
      />
    </div>

    <p class="text-lg">{{ skill.category || 'Описание отсутствует' }}</p>

    <!-- Отображаем текущий уровень -->
    <div v-if="userSkill" class="mt-4">
      <p class="text-lg">Текущий уровень: {{ userSkill.level }}</p>
    </div>

    <Button label="Пройти заново" icon="pi pi-refresh" class="mt-4 p-button-lg" @click="toggleTest" />

    <!-- Контейнер для теста -->
    <div v-if="showTest" class="mt-4">
        <h2 class="text-2xl font-bold mb-2">Прохождение теста</h2>
        <iframe v-if="skill.test" :src="skill.test" class="test-iframe border-round shadow-1"></iframe>
        <p v-else class="text-lg text-center">Ссылка на тест отсутствует</p>
      </div>
  
      <!-- Кнопка завершить тест -->
      <div v-if="showTest">
        <Button label="Завершить" icon="pi pi-check" class="mt-4 p-button-success" @click="recompleteTest" />
      </div>
    </div>
  
</template>

<script setup>
import { ref, onMounted, defineProps } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../utils/api'
const isLogin = ref(true)
const route = useRoute()
const router = useRouter()
const skill = ref({})
const showTest = ref(false)
const userSkill = ref(null)
const user = ref({})

const loadSkill = async () => {
    try{
        const { me } = await api.get('/auth/users/me/')
        user.value = me
        
    } catch (error)
    { console.error('Не зареган', error)}
    try {

      const { data } = await api.get(`/skills/${route.params.id}/`)
      skill.value = data
      console.log(skill.value.id)
    } catch (error) {
      console.error('Ошибка загрузки навыка:', error)
    }
    try {
      const { dataIt } = await api.get(`/user-skill/?user_id=${user.value.id}&skill_id=${skill.value.id}/`)
      userSkill.value = dataIt
      } catch (error) {
      console.error('Ошибка загрузки навыка пользователя:', error)
}
  }

const toggleTest = () => {
  showTest.value = !showTest.value
}

const recompleteTest = async () => {
  try {
    // Создаем случайное число от 1 до 10 для уровня
    const level = Math.floor(Math.random() * 10) + 1
    
    // Отправляем PUT запрос для обновления уровня навыка пользователя
    await api.put(`/user-skill/${userSkill.value.id}/`, {
      id: userSkill.value.id,
      user_id: user.value.id,
      skill_id: skill.value.id,
      level: level,
    })

    // Оповещаем пользователя о завершении теста
    alert('Вы успешно обновили уровень навыка.')

    // Переходим на страницу профиля после завершения теста
    router.push('/profile') // Это будет путь к странице профиля, при необходимости можно изменить
  } catch (error) {
    console.error('Ошибка обновления уровня навыка:', error)
  }
}

onMounted(loadSkill)
</script>

<style scoped>
.test-iframe {
  width: 80%;
  height: 600px;
  border: none;
  transform: scale(0.8);
  transform-origin: 0 0;
  pointer-events: auto;
  overflow: hidden;
}
</style>
