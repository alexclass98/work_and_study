<template>
  <div class="card flex justify-content-center">
    <div class="surface-card p-4 shadow-2 border-round w-full lg:w-6">
      <div class="text-center mb-5">
        <h1 class="text-3xl font-medium text-900 mb-3">{{ isLogin ? 'Вход' : 'Регистрация' }}</h1>
      </div>

      <form @submit.prevent="submitForm">
        <div class="field">
          <label class="block text-900 font-medium mb-2">Имя пользователя</label>
          <InputText v-model="form.username" class="w-full" />
        </div>

        <div v-if="!isLogin" class="field">
          <label class="block text-900 font-medium mb-2">Email</label>
          <InputText v-model="form.email" class="w-full" />
        </div>

        <div class="field">
          <label class="block text-900 font-medium mb-2">Пароль</label>
          <Password v-model="form.password" class="w-full" />
        </div>

        <Button
            :label="isLogin ? 'Войти' : 'Зарегистрироваться'"
            class="w-full mt-3"
            type="submit"
        />

        <div class="text-center mt-3">
          <a
              @click="isLogin = !isLogin"
              class="text-primary cursor-pointer"
          >
            {{ isLogin ? 'Нет аккаунта? Зарегистрироваться' : 'Уже есть аккаунт? Войти' }}
          </a>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import api from '../utils/api'

const router = useRouter()
const isLogin = ref(true)
const form = ref({
  username: '',
  email: '',
  password: ''
})

const submitForm = async () => {
  const formData = new FormData()
  formData.append('username', form.value.username)
  formData.append('password', form.value.password)

  if (!isLogin.value) {
    formData.append('email', form.value.email)
  }

  try {
    if (isLogin.value) {
      // Логин
      const response = await api.post('/auth/jwt/create/', formData)
      const { access, refresh } = response.data
      console.log('Access Token:', access) // Логируем токен
      console.log('Refresh Token:', refresh) // Логируем refresh-токен
      localStorage.setItem('accessToken', access)
      localStorage.setItem('refreshToken', refresh) // Сохраняем refresh-токен
      router.push('/')
    } else {
      // Регистрация
      await api.post('/auth/users/', formData)
      isLogin.value = true
    }
  } catch (error) {
    console.error('Authentication error:', error)
    alert('Ошибка при авторизации. Проверьте данные и подключение к серверу.')
  }
}
</script>