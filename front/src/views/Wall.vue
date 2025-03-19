<template>
  <div class="surface-ground p-3">
    <div class="surface-card shadow-2 p-3 border-round">
      <h1 class="text-3xl mb-5">Общая лента</h1>

      <div class="grid">
        <div class="col-12 lg:col-8 lg:col-offset-2">
          <div class="flex flex-column gap-3">
            <div v-for="message in messages" :key="message.id" class="p-3 surface-section border-round shadow-1">
              <div class="flex align-items-center mb-2">
                <Avatar :label="getUserInitials(message.author)" class="mr-2" />
                <div>
                  <div class="font-bold">{{ getUserName(message.author) }}</div>
                  <div class="text-sm text-color-secondary">
                    {{ formatDate(message.timestamp) }}
                  </div>
                </div>
              </div>
              <div class="ml-5">
                <h4 class="mt-0 mb-2">{{ message.topic }}</h4>
                <p class="mt-0">{{ message.text }}</p>
              </div>
            </div>
          </div>

          <div class="mt-5 p-3 surface-section border-round shadow-2">
            <InputText v-model="newMessage.topic" placeholder="Тема сообщения" class="w-full mb-3" />
            <Textarea v-model="newMessage.text" rows="3" class="w-full mb-3" />
            <Button label="Отправить" icon="pi pi-send" @click="sendMessage" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import api from '../utils/api'

const router = useRouter()
const messages = ref([])
const newMessage = ref({ topic: '', text: '' })
const ws = ref(null)
const usersCache = ref({})

const connectWebSocket = () => {
  try {
    ws.value = new WebSocket('ws://localhost:8000/ws/wall/')

    ws.value.onopen = () => {
      console.log('WebSocket подключен')
    }

    ws.value.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data)
        messages.value = [message, ...messages.value]
        fetchUser(message.author)
      } catch (e) {
        console.error('Ошибка обработки сообщения:', e)
      }
    }

    ws.value.onerror = (error) => {
      console.error('WebSocket error:', error)
      //setTimeout(connectWebSocket, 3000)
    }

    ws.value.onclose = () => {
      console.log('WebSocket закрыт. Переподключение...')
      //setTimeout(connectWebSocket, 5000)
    }
  } catch (e) {
    console.error('Ошибка создания WebSocket:', e)
  }
}

const fetchUser = async (userId) => {
  if (!usersCache.value[userId]) {
    try {
      const response = await api.get(`/users/${userId}/`)
      usersCache.value[userId] = response.data
    } catch (error) {
      console.error('Ошибка загрузки пользователя:', error)
    }
  }
}

const getUserInitials = (userId) => {
  const user = usersCache.value[userId]
  if (!user || !user.first_name || !user.last_name) return '??'
  return `${user.first_name[0]?.toUpperCase() ?? ''}${user.last_name[0]?.toUpperCase() ?? ''}`
}

const getUserName = (userId) => {
  const user = usersCache.value[userId]
  return user ? `${user.first_name} ${user.last_name}` : 'Неизвестный пользователь'
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleString()
}

const loadMessages = async () => {
  try {
    const response = await api.get('/messages/')
    messages.value = response.data.reverse()

    // Кэшируем информацию о пользователях
    const userIds = [...new Set(messages.value.map(m => m.author))]
    const usersRes = await api.post('/users/by_ids/', { ids: userIds })
    usersRes.data.forEach(user => {
      usersCache.value[user.id] = user
    })
  } catch (error) {
    console.error('Ошибка загрузки сообщений:', error)
  }
}

const sendMessage = async () => {
  if (!newMessage.value.text.trim()) return

  try {
    const response = await api.post('/messages/', {
      ...newMessage.value,
      author: user.value.id
    })

    newMessage.value = { topic: '', text: '' }
  } catch (error) {
    console.error('Ошибка отправки сообщения:', error)
  }
}

onMounted(() => {
  loadMessages()
  connectWebSocket()
})

onBeforeUnmount(() => {
  if (ws.value) ws.value.close()
})
</script>