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
  
      <Button label="Начать тестирование" icon="pi pi-play" class="mt-4 p-button-lg" @click="toggleTest" />
  
      <!-- Контейнер для теста -->
      <div v-if="showTest" class="mt-4">
        <h2 class="text-2xl font-bold mb-2">Прохождение теста</h2>
        <iframe v-if="skill.test" :src="skill.test" class="test-iframe border-round shadow-1"></iframe>
        <p v-else class="text-lg text-center">Ссылка на тест отсутствует</p>
      </div>
  
      <!-- Кнопка завершить тест -->
      <div v-if="showTest">
        <Button label="Завершить" icon="pi pi-check" class="mt-4 p-button-success" @click="completeTest" />
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import api from '../utils/api'
  
  const route = useRoute()
  const router = useRouter()
  const skill = ref({})
  const showTest = ref(false)
  
  const loadSkill = async () => {
    try{
        const { me } = await api.get('/auth/users/me/')
        user.value = me
    } catch (error)
    { console.error('Не зареган', error)}
    try {

      const { data } = await api.get(`/skills/${route.params.id}/`)
      skill.value = data
    } catch (error) {
      console.error('Ошибка загрузки навыка:', error)
    }
  }
  
  const toggleTest = () => {
    showTest.value = !showTest.value
  }
  
  const completeTest = async () => {
    try {
      // Создаем случайное число от 1 до 10 для level
      const level = Math.floor(Math.random() * 10) + 1
      
      // Делаем запрос для создания записи в таблице user-skill
      await api.post('/user-skill/', {
        user_id: user.value.id, // В будущем будет динамическим значением
        skill_id: skill.value.id,
        level: level,
      })
  
      // Оповещаем пользователя о завершении теста
      alert('Тест завершен, уровень навыка был случайным образом установлен.')
  
      // После завершения теста, переходим на страницу профиля
      router.push('/profile') // Это будет путь к странице профиля, при необходимости можно изменить
    } catch (error) {
      console.error('Ошибка завершения теста:', error)
    }
  }
  
  onMounted(loadSkill)
  </script>
  
  <style scoped>
  .test-iframe {
    width: 80%;
    height: 600px; /* Размер iframe */
    border: none;
    transform: scale(0.8); /* Уменьшаем масштаб */
    transform-origin: 0 0; /* Устанавливаем точку отсчета для масштабирования */
    pointer-events: auto;
    overflow: hidden; /* Отключаем прокрутку */
  }
  </style>
  