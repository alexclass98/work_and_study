<template>
  <div class="p-3 surface-section border-round shadow-1">
    <div class="flex align-items-center mb-2">
      <!-- Avatar: Uses computed property for better reactivity and default handling -->
      <Avatar
          :label="authorInitials"
          shape="circle"
          class="mr-2 flex-shrink-0"
          :style="{ backgroundColor: getAvatarColor(message.author), color: '#ffffff' }"
      />
      <div>
        <!-- Author Name: Uses computed property -->
        <div class="font-bold">{{ authorName }}</div>
        <!-- Date: Uses computed property and assumes 'date_send' field -->
        <div class="text-sm text-color-secondary">{{ formattedTimestamp }}</div>
      </div>
    </div>
    <div class="ml-5"> <!-- This maintains the indentation for content and replies -->
      <h4 v-if="message.topic" class="mt-0 mb-2 text-lg">{{ message.topic }}</h4>
      <p class="mt-0 mb-2 line-height-3">{{ message.text }}</p>
      <Button
          label="Ответить"
          icon="pi pi-reply"
          @click="toggleReplyForm"
          class="p-button-sm"
      />

      <!-- Reply Form -->
      <div v-if="showReplyForm" class="mt-3">
        <!-- Using Textarea for potentially longer replies -->
        <Textarea v-model="replyText" rows="2" class="w-full mb-2" placeholder="Введите ответ..." autoResize/>
        <div class="flex gap-2">
          <Button
              label="Отправить"
              icon="pi pi-send"
              @click="sendReply"
              :loading="sendingReply"
              :disabled="!replyText.trim() || sendingReply"
              class="p-button-sm"
          />
          <Button
              label="Отмена"
              @click="cancelReply"
              class="p-button-sm p-button-secondary"
          />
        </div>
      </div>

      <!-- Recursive rendering of replies -->
      <div v-if="message.replies && message.replies.length" class="mt-3 pl-4 border-left-2 surface-border">
        <!-- Pass usersCache down to replies -->
        <MessageItem
            v-for="reply in message.replies"
            :key="reply.id"
            :message="reply"
            :usersCache="usersCache"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, ref, computed, onMounted } from 'vue';
import api from '../utils/api';

// --- PrimeVue Component Imports ---
import Avatar from 'primevue/avatar';
import Button from 'primevue/button';
import InputText from 'primevue/inputtext'; // Keep if used, though Textarea might be better for replies
import Textarea from 'primevue/textarea'; // Added for reply form

// --- Import self for recursion ---
import MessageItem from './MessageItem.vue';

// --- Props ---
const props = defineProps({
  message: {
    type: Object,
    required: true
  },
  usersCache: {
    type: Object,
    required: true
  }
});

// --- State ---
const showReplyForm = ref(false);
const replyText = ref('');
const sendingReply = ref(false);
const currentUser = ref(null); // Store current user data for sending replies

// --- Computed Properties for Display ---
const author = computed(() => {
  // Safely get the author object from cache
  return props.message?.author && props.usersCache?.[props.message.author]
      ? props.usersCache[props.message.author]
      : null;
});

const authorName = computed(() => {
  // Display full name if available, otherwise username, or fallback
  if (author.value?.first_name && author.value?.last_name) {
    // Check for non-empty strings
    const fn = author.value.first_name.trim();
    const ln = author.value.last_name.trim();
    if (fn && ln) return `${fn} ${ln}`;
    if (fn) return fn;
    if (ln) return ln;
  }
  return author.value?.username ?? 'Неизвестный пользователь';
});

const authorInitials = computed(() => {
  // Generate initials, preferring first/last name, fallback to username
  const fn = author.value?.first_name?.[0]?.toUpperCase();
  const ln = author.value?.last_name?.[0]?.toUpperCase();

  if (fn && ln) return fn + ln;
  if (fn) return fn;
  if (ln) return ln;
  if (author.value?.username) return author.value.username[0].toUpperCase();
  return '?';
});

const formattedTimestamp = computed(() => {
  // Format date, assuming 'date_send' field from backend message object
  const dateString = props.message?.date_send; // Use the correct field name
  if (!dateString) return '';
  try {
    return new Date(dateString).toLocaleString('ru-RU', {
      dateStyle: 'short',
      timeStyle: 'short'
    });
  } catch (e) {
    console.error("Error formatting date:", e);
    return dateString; // Return original string if formatting fails
  }
});

// --- Methods ---
const toggleReplyForm = () => {
  showReplyForm.value = !showReplyForm.value;
  if (!showReplyForm.value) {
    replyText.value = ''; // Clear text if closing
  }
};

const cancelReply = () => {
  showReplyForm.value = false;
  replyText.value = '';
};

const sendReply = async () => {
  if (!replyText.value.trim() || !currentUser.value?.id) {
    if(!currentUser.value?.id) alert("Не удалось определить пользователя. Войдите снова.");
    return;
  }

  sendingReply.value = true;

  // --- Send JSON payload (recommended for DRF) ---
  const payload = {
    parent_message_id: props.message.id,
    text: replyText.value.trim(),
    topic: props.message.topic.startsWith('Re: ') ? props.message.topic : `Re: ${props.message.topic}`, // Avoid multiple "Re:"
    author: currentUser.value.id
  };

  try {
    // Use JSON post request
    const response = await api.post('/messages/', payload);

    // --- Add reply reactively (no page reload) ---
    if (!props.message.replies) {
      props.message.replies = [];
    }
    props.message.replies.push(response.data);

    // Ensure current user is cached if not already (for the new reply author)
    if (!props.usersCache[currentUser.value.id]) {
      props.usersCache[currentUser.value.id] = currentUser.value;
    }

    cancelReply(); // Close form and clear text

  } catch (error) {
    console.error('Ошибка отправки ответа:', error);
    alert(`Ошибка ответа: ${error.response?.data?.detail || JSON.stringify(error.response?.data) || error.message}`);
  } finally {
    sendingReply.value = false;
  }
};

// Simple hash function for color generation consistency
const stringHashCode = (str) => {
  let hash = 0;
  if (!str || str.length === 0) return hash;
  for (let i = 0; i < str.length; i++) {
    const char = str.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash |= 0; // Convert to 32bit integer
  }
  return hash;
};

// Generate a consistent color based on user ID
const getAvatarColor = (userId) => {
  if (!userId) return '#dee2e6'; // Default grey
  // Consistent color palette
  const colors = ['#0D9276', '#40A578', '#9DDE8B', '#E6FF94', '#1B4242', '#5C8374', '#93B1A6', '#FF6B6B'];
  // Use hash code for a more stable color assignment than just modulo
  const index = Math.abs(stringHashCode(String(userId))) % colors.length;
  return colors[index];
};

// Fetch current user when the component mounts to get the ID for sending replies
onMounted(async () => {
  try {
    const { data } = await api.get('/auth/users/me/');
    currentUser.value = data;
  } catch (error) {
    console.error('Ошибка получения текущего пользователя в MessageItem:', error);
    // Maybe handle the case where user is not logged in and disable reply?
  }
});
</script>

<style scoped>
/* Minimal styles to keep close to original request */
.p-avatar {
  font-weight: bold;
}
.border-left-2 {
  border-left: 2px solid var(--surface-border) !important;
}
.flex-shrink-0 {
  flex-shrink: 0; /* Prevent avatar shrinking on small screens */
}
</style>