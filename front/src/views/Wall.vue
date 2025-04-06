<template>
  <div class="surface-ground p-3 lg:p-4">
    <div class="surface-card shadow-2 p-4 lg:p-5 border-round">
      <h1 class="text-3xl p-m-0 p-mb-5">Общая лента</h1>
      <!-- Исправленная строка v-if и класса -->
      <p v-if="wsStatus !== 'connected'" class="text-orange-600 p-mb-4">
        <i class="pi pi-exclamation-triangle p-mr-1"></i> WebSocket не подключен ({{ wsStatus }}). Обновления в реальном времени могут не работать.
      </p>
      <div class="p-mb-5 p-p-4 surface-100 border-round">
        <h3 class="p-mt-0 p-mb-3">Новое сообщение</h3>
        <div class="p-fluid">
          <div class="p-field p-mb-3">
            <label for="topic" class="p-d-block p-mb-1">Тема</label>
            <InputText id="topic" v-model="newMessage.topic" placeholder="Введите тему" class="w-full" />
          </div>
          <div class="p-field p-mb-3">
            <label for="text" class="p-d-block p-mb-1">Текст сообщения</label>
            <Textarea id="text" v-model="newMessage.text" rows="3" placeholder="Введите текст" class="w-full" autoResize />
          </div>
          <Button label="Отправить" icon="pi pi-send" @click="sendMessage" :disabled="!newMessage.text.trim() || !currentUser" :loading="sending"/>
        </div>
      </div>

      <div v-if="loadingMessages" class="p-d-flex p-jc-center p-p-5">
        <ProgressSpinner animationDuration=".5s"/>
      </div>
      <div v-else class="p-grid">
        <div class="p-col-12 lg:p-col-10 lg:p-col-offset-1 xl:p-col-8 xl:p-col-offset-2">
          <div class="p-d-flex p-flex-column p-gap-3">
            <div v-if="structuredMessages.length === 0" class="text-center text-600 p-p-5">
              Сообщений пока нет.
            </div>
            <MessageItem
                v-for="message in structuredMessages"
                :key="message.id"
                :message="message"
                :usersCache="usersCache"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, computed } from 'vue';
import api from '../utils/api';
import MessageItem from './MessageItem.vue';

import InputText from 'primevue/inputtext';
import Textarea from 'primevue/textarea';
import Button from 'primevue/button';
import ProgressSpinner from 'primevue/progressspinner';

const messages = ref([]);
const newMessage = ref({ topic: '', text: '' });
const usersCache = ref({});
const loadingMessages = ref(true);
const sending = ref(false);
const currentUser = ref(null);
const wallSocket = ref(null);
const wsStatus = ref('disconnected');

const BACKEND_HOST = 'localhost:8000';

const loadCurrentUser = async () => {
  try {
    const { data } = await api.get('/auth/users/me/');
    currentUser.value = data;
  } catch (error) {
    console.error('Ошибка получения текущего пользователя:', error);
  }
};

const loadMessagesAndUsers = async () => {
  loadingMessages.value = true;
  try {
    const messagesResponse = await api.get('/messages/');
    messages.value = messagesResponse.data.sort((a, b) => new Date(b.date_send) - new Date(a.date_send));

    const userIds = [...new Set(messages.value.map(m => m.author).filter(id => id != null))];
    if (userIds.length > 0) {
      await fetchUsers(userIds);
    }
  } catch (error) {
    console.error('Ошибка загрузки сообщений:', error);
  } finally {
    loadingMessages.value = false;
  }
};

const fetchUsers = async (userIds) => {
  const idsToFetch = userIds.filter(id => !usersCache.value[id]);
  if (idsToFetch.length === 0) return;

  try {
    const usersRes = await api.post('/users/by_ids/', { ids: idsToFetch });
    usersRes.data.forEach(user => {
      usersCache.value[user.id] = user;
    });
  } catch (error) {
    console.error('Ошибка загрузки пользователей:', error);
  }
};

const structuredMessages = computed(() => {
  const map = {};
  const msgs = messages.value || [];
  msgs.forEach(msg => { if(msg && msg.id) map[msg.id] = { ...msg, replies: [] }; });
  const rootMessages = [];
  msgs.forEach(msg => {
    if (msg && msg.id) {
      if (msg.parent_message_id && map[msg.parent_message_id]) {
        if (!map[msg.parent_message_id].replies) {
          map[msg.parent_message_id].replies = [];
        }
        map[msg.parent_message_id].replies.push(map[msg.id]);
      } else if (!msg.parent_message_id) {
        rootMessages.push(map[msg.id]);
      }
    }
  });
  Object.values(map).forEach(msg => {
    if (msg.replies?.length > 1) {
      msg.replies.sort((a, b) => new Date(a.date_send) - new Date(b.date_send));
    }
  });
  return rootMessages;
});

const sendMessage = async () => {
  if (!newMessage.value.text.trim() || !currentUser.value?.id) return;
  sending.value = true;
  const payload = {
    text: newMessage.value.text,
    topic: newMessage.value.topic || 'Без темы',
    author: currentUser.value.id, // Отправляем ID, но бэк все равно его установит из request.user
    parent_message_id: 0 // Попробуем отправить 0 вместо null
  };
  try {
    await api.post('/messages/', payload);
    newMessage.value.text = '';
    newMessage.value.topic = '';
  } catch (error) {
    console.error('Ошибка отправки сообщения:', error);
    alert(`Ошибка отправки: ${error.response?.data?.detail || JSON.stringify(error.response?.data) || error.message}`);
  } finally {
    sending.value = false;
  }
};

const connectWebSocket = () => {
  const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';

  const wsUrl = `${wsProtocol}//${BACKEND_HOST}/ws/wall/`;

  console.log(`Connecting to WebSocket: ${wsUrl}`);
  wsStatus.value = 'connecting';

  // Закрываем старое соединение, если оно есть
  if (wallSocket.value) {
    wallSocket.value.close();
  }

  wallSocket.value = new WebSocket(wsUrl);

  wallSocket.value.onopen = () => {
    console.log("WebSocket connected successfully.");
    wsStatus.value = 'connected';
  };

  wallSocket.value.onmessage = (event) => {
    console.log("WebSocket message received:", event.data);
    try {
      const data = JSON.parse(event.data);

      if (data.type === 'new_message' && data.message) {
        const newMessageData = data.message;
        const authorDetails = data.author_details;

        if (authorDetails && authorDetails.id) {
          usersCache.value[authorDetails.id] = authorDetails;
        }

        // Добавляем сообщение в массив, если его еще нет
        const exists = messages.value.some(m => m.id === newMessageData.id);
        if (!exists) {
          messages.value.unshift(newMessageData); // Добавляем новое сообщение в начало
          console.log("New message added to messages array.");
        } else {
          console.log("Duplicate message received.");
        }
      }
    } catch (e) {
      console.error("Failed to parse WebSocket message or invalid format:", e);
    }
  };

  wallSocket.value.onerror = (error) => {
    console.error("WebSocket error:", error);
    wsStatus.value = 'error';
  };

  wallSocket.value.onclose = (event) => {
    console.log("WebSocket closed:", event.code, event.reason);
    wsStatus.value = 'disconnected';
    wallSocket.value = null;
    // Optional reconnect logic
    // if (event.code !== 1000) { // Don't reconnect on normal close
    //    console.log("Attempting to reconnect WebSocket...");
    //    setTimeout(connectWebSocket, 5000);
    // }
  };
};

const disconnectWebSocket = () => {
  if (wallSocket.value) {
    console.log("Closing WebSocket connection.");
    // Устанавливаем код 1000 для нормального закрытия, чтобы избежать авто-реконнекта (если он есть)
    wallSocket.value.close(1000, "Component Unmounted");
    wallSocket.value = null;
  }
};

onMounted(async () => {
  await loadCurrentUser();
  await loadMessagesAndUsers();
  connectWebSocket();
});

onBeforeUnmount(() => {
  disconnectWebSocket();
});

</script>

<style scoped>
/* Your component styles */
</style>