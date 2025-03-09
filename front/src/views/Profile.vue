<template>
  <div class="profile">
    <h1>Профиль пользователя</h1>
    <p>Здесь будет информация о пользователе.</p>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// Проверка авторизации при загрузке страницы
onMounted(() => {
  const isAuthenticated = localStorage.getItem('accessToken')
  if (!isAuthenticated) {
    router.push('/auth')
  }
})
</script>

<style scoped>
.profile {
  padding: 2rem;
  text-align: center;
}
</style>