<template>
  <div class="surface-ground p-3">
    <div class="surface-card shadow-2 p-3 border-round">
      <h1 class="text-3xl mb-5">Общая лента</h1>
      <div class="mt-5 p-3 surface-section border-round shadow-2">
        <InputText v-model="newMessage.topic" placeholder="Тема сообщения" class="w-full mb-3" />
        <InputText v-model="newMessage.text"  rows="3" placeholder="Текст" class="w-full mb-3" />

        <Button label="Отправить" icon="pi pi-send" @click="sendMessage" />
      </div>
      <div class="mt-5 p-3 grid">
        <div class="col-12 lg:col-8 lg:col-offset-2">
          <div class="flex flex-column gap-3">
            <div v-for="message in structuredMessages" :key="message.id" class="p-3 surface-section border-round shadow-1">
              <MessageItem :message="message" :usersCache="usersCache" @reply="replyToMessage" />
            </div>
          </div>


        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, computed, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import api from '../utils/api'
import MessageItem from './MessageItem.vue'

const router = useRouter()
const messages = ref([])
const newMessage = ref({ topic: '', text: '' })
const replyMessage = ref({ topic: '', text: '', parent_message_id: null })
const usersCache = ref({})
const showReplyForm = ref(false)
const messageInput = ref(null)
const isLogin = ref(true)

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

const loadMessages = async () => {
  try {
    const response = await api.get('/messages/')
    messages.value = response.data.reverse()

    const userIds = [...new Set(messages.value.map(m => m.author))]
    const usersRes = await api.post('/users/by_ids/', { ids: userIds })
    usersRes.data.forEach(user => {
      usersCache.value[user.id] = user
    })
  } catch (error) {
    console.error('Ошибка загрузки сообщений:', error)
  }
}

const structuredMessages = computed(() => {
  const map = {}
  messages.value.forEach(msg => (map[msg.id] = { ...msg, replies: [] }))

  const rootMessages = []
  messages.value.forEach(msg => {
    if (msg.parent_message_id && map[msg.parent_message_id]) {
      map[msg.parent_message_id].replies.push(map[msg.id])
    } else {
      rootMessages.push(map[msg.id])
    }
  })
  return rootMessages
})

const sendMessage = async () => {
  const formData = new FormData();
  formData.append('parent_message_id', 0);
  formData.append('text', newMessage.value.text);
  formData.append('topic', newMessage.value.topic);

  try {
    const { data } = await api.get('/auth/users/me/');
    formData.append('author', data.id);
  } catch (error) {
    console.error('Ошибка получения пользователя', error);
  }

  try {
    await api.post('/messages/', formData);
    isLogin.value = true;
    location.reload();
    newMessage.value.text = '';
    newMessage.value.topic = '';
  } catch (error) {
    console.error('Ошибка отправки сообщения:', error);
  }
}

const replyToMessage = (message) => {
  replyMessage.value.topic = `Ответ на: ${message.topic}`;
  replyMessage.value.parent_message_id = message.id;
  replyMessage.value.text = '';
  showReplyForm.value = true;

  nextTick(() => {
    if (messageInput.value) {
      messageInput.value.focus();
    }
  });
}

onMounted(() => {
  loadMessages();
})
</script>
