<template>
  <div class="card flex justify-content-center p-fluid">
    <div class="surface-card p-4 shadow-2 border-round w-full lg:w-6">
      <div class="text-center mb-5">
        <h1 class="text-3xl font-medium text-900 mb-3">Завершение регистрации: Шаг 2 из 2</h1>
        <p>Пожалуйста, заполните дополнительную информацию о себе.</p>
      </div>

      <form v-if="!loadingInitial && user" @submit.prevent="submitProfileData">
        <div class="field">
          <label for="surname" class="block text-900 font-medium mb-2">Фамилия</label>
          <InputText id="surname" v-model="profileForm.surname" class="w-full" />
        </div>
        <div class="field">
          <label for="middlename" class="block text-900 font-medium mb-2">Отчество</label>
          <InputText id="middlename" v-model="profileForm.middlename" class="w-full" />
        </div>
        <div class="field">
          <label for="gender" class="block text-900 font-medium mb-2">Пол</label>
          <Dropdown id="gender" v-model="profileForm.gender" :options="genderOptions" optionLabel="label" optionValue="value" placeholder="Выберите пол" class="w-full" />
        </div>
        <div class="field">
          <label for="dob" class="block text-900 font-medium mb-2">Дата рождения</label>
          <Calendar id="dob" v-model="profileForm.dd_mm_yy" dateFormat="yy-mm-dd" class="w-full" placeholder="ГГГГ-ММ-ДД" :showIcon="true"/>
        </div>
        <div class="field">
          <label for="city" class="block text-900 font-medium mb-2">Город</label>
          <InputText id="city" v-model="profileForm.city" class="w-full" />
        </div>
        <div class="field">
          <label for="country" class="block text-900 font-medium mb-2">Страна</label>
          <InputText id="country" v-model="profileForm.country" class="w-full" />
        </div>

        <Message v-if="errorMessage" severity="error" :closable="false" class="mt-3">{{ errorMessage }}</Message>

        <Button label="Завершить регистрацию" class="w-full mt-3" type="submit" :loading="loadingSubmit"/>
      </form>

      <div v-else-if="loadingInitial" class="text-center">
        <ProgressSpinner style="width:50px;height:50px" strokeWidth="8" />
        <p>Загрузка данных...</p>
      </div>
      <div v-else class="text-center">
        <Message severity="warn">Не удалось загрузить данные пользователя. Пожалуйста, убедитесь, что вы вошли в систему.</Message>
        <Button label="Перейти ко входу" @click="goToLogin" class="p-button-secondary mt-3"/>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '../utils/api';

import InputText from 'primevue/inputtext';
import Dropdown from 'primevue/dropdown';
import Calendar from 'primevue/calendar';
import Button from 'primevue/button';
import Message from 'primevue/message';
import ProgressSpinner from 'primevue/progressspinner';

const router = useRouter();
const user = ref(null);
const loadingInitial = ref(true);
const loadingSubmit = ref(false);
const errorMessage = ref('');

const profileForm = ref({
  surname: '',
  middlename: '',
  gender: null,
  dd_mm_yy: null,
  city: '',
  country: ''
});

const genderOptions = ref([
  { label: 'Мужской', value: true },
  { label: 'Женский', value: false }
]);

const handleApiError = (error, context = 'submit') => {
  if (context === 'submit') loadingSubmit.value = false;
  else loadingInitial.value = false;

  console.error(`API Error (${context}):`, error);
  if (error.response) {
    console.error('Error data:', error.response.data);
    const errorData = error.response.data;
    if (typeof errorData === 'object' && errorData !== null) {
      errorMessage.value = Object.entries(errorData).map(([key, value]) =>
          `${key}: ${Array.isArray(value) ? value.join(' ') : value}`
      ).join('\n');
    } else {
      errorMessage.value = `Ошибка сервера (${error.response.status})`;
    }
  } else if (error.request) {
    errorMessage.value = 'Сервер не отвечает.';
  } else {
    errorMessage.value = error.message || 'Неизвестная ошибка.';
  }
};

onMounted(async () => {
  loadingInitial.value = true;
  errorMessage.value = '';
  try {
    const response = await api.get('/auth/users/me/');
    user.value = response.data;
    if (!user.value || !user.value.id) {
      throw new Error("Не удалось получить ID пользователя.");
    }
  } catch (error) {
    handleApiError(error, 'initial load');
  } finally {
    loadingInitial.value = false;
  }
});

const submitProfileData = async () => {
  if (!user.value || !user.value.id) {
    errorMessage.value = "Ошибка: ID пользователя не определен.";
    return;
  }

  loadingSubmit.value = true;
  errorMessage.value = '';

  try {
    const payload = {
      user_id: user.value.id,
      gender: profileForm.value.gender,
      city: profileForm.value.city,
      country: profileForm.value.country,
      dd_mm_yy: profileForm.value.dd_mm_yy
          ? profileForm.value.dd_mm_yy.toISOString().split('T')[0]
          : null,
      surname: profileForm.value.surname,
      middlename: profileForm.value.middlename
    };

    const cleanedPayload = { user_id: payload.user_id };
    for (const key in payload) {
      if (key !== 'user_id' && payload[key] !== null && payload[key] !== '') {
        cleanedPayload[key] = payload[key];
      }
    }
    // Explicitly add dd_mm_yy back if it was set, even if to null, IF your backend accepts null
    // If backend requires the field only if it has a value, keep the line below commented/removed.
    // if (payload.dd_mm_yy === null && profileForm.value.dd_mm_yy !== undefined) cleanedPayload.dd_mm_yy = null;


    await api.post('/form/', cleanedPayload);

    router.push('/profile');

  } catch (error) {
    handleApiError(error, 'submit');
  } finally {
    loadingSubmit.value = false;
  }
};

const goToLogin = () => {
  router.push('/login');
}

</script>

<style scoped>
/* Add styles if needed */
</style>