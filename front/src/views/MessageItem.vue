<template>
  <div class="p-3 surface-section border-round shadow-1">
    <div class="flex align-items-center mb-2">
      <Avatar :label="getUserInitials(message.author)" class="mr-2" />
      <div>
        <div class="font-bold">{{ getUserName(message.author) }}</div>
        <div class="text-sm text-color-secondary">{{ formatDate(message.timestamp) }}</div>
      </div>
    </div>
    <div class="ml-5">
      <h4 class="mt-0 mb-2">{{ message.topic }}</h4>
      <p class="mt-0">{{ message.text }}</p>
      <Button label="Ответить" icon="pi pi-reply" @click="toggleReplyForm"  />

      <!-- Форма ответа -->
      <div v-if="showReplyForm" class="mt-3">
        <Textarea v-model="replyText" rows="2" class="w-full mb-2" placeholder="Введите ответ..." />
        <div class="flex gap-2">
          <Button label="Отправить" icon="pi pi-send" @click="sendReply" :disabled="!replyText.trim()" />
          <Button label="Отмена" @click="cancelReply" />
        </div>
      </div>

      <!-- Рекурсивный рендеринг ответов -->
      <div v-if="message.replies.length" class="mt-3 pl-5 border-left-2">
        <MessageItem v-for="reply in message.replies" :key="reply.id" :message="reply" :usersCache="usersCache" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, ref } from 'vue'
import api from '../utils/api'

const props = defineProps({
  message: Object,
  usersCache: Object
})

const showReplyForm = ref(false)
const replyText = ref('')

const toggleReplyForm = () => {
  showReplyForm.value = !showReplyForm.value
}

const cancelReply = () => {
  showReplyForm.value = false
  replyText.value = ''
}

const sendReply = async () => {
  if (!replyText.value.trim()) return

  try {
    await api.post('/messages/', {
      topic: `Ответ на: ${props.message.topic}`,
      text: replyText.value,
      parent_message_id: props.message.id,
      author: 222 // здесь должен быть ID текущего пользователя
    })
    cancelReply()
  } catch (error) {
    console.error('Ошибка отправки ответа:', error)
  }
}

const getUserInitials = (userId) => {
  const user = props.usersCache[userId]
  if (!user || !user.first_name || !user.last_name) return '??'
  return `${user.first_name[0]?.toUpperCase() ?? ''}${user.last_name[0]?.toUpperCase() ?? ''}`
}

const getUserName = (userId) => {
  const user = props.usersCache[userId]
  return user ? `${user.first_name} ${user.last_name}` : 'Неизвестный пользователь'
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleString()
}
</script>
