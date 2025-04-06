<template>
  <div class="card flex justify-content-center">
    <div class="surface-card p-4 shadow-2 border-round w-full lg:w-6">
      <div class="text-center mb-5">
        <h1 class="text-3xl font-medium text-900 mb-3">{{ viewMode === 'login' ? 'Вход' : 'Регистрация: Шаг 1 из 2' }}</h1>
        <p v-if="viewMode === 'register'">Введите основные данные для создания аккаунта.</p>
      </div>

      <form v-if="viewMode === 'login'" @submit.prevent="submitLogin">
        <div class="field">
          <label class="block text-900 font-medium mb-2">Имя пользователя</label>
          <InputText v-model="loginForm.username" class="w-full" required />
        </div>
        <div class="field">
          <label class="block text-900 font-medium mb-2">Пароль</label>
          <Password v-model="loginForm.password" class="w-full custom-password" required toggleMask :feedback="false"/>
        </div>
        <Button label="Войти" class="w-full mt-3" type="submit" :loading="loading"/>
        <div class="text-center mt-3">
          <a @click="switchToRegister" class="text-primary cursor-pointer">
            Нет аккаунта? Зарегистрироваться
          </a>
        </div>
      </form>

      <form v-if="viewMode === 'register'" @submit.prevent="submitRegistrationStep1">
        <div class="field">
          <label class="block text-900 font-medium mb-2">Имя пользователя</label>
          <InputText v-model="registerForm.username" class="w-full" required />
        </div>
        <div class="field">
          <label class="block text-900 font-medium mb-2">Email</label>
          <InputText type="email" v-model="registerForm.email" class="w-full" required />
        </div>
        <div class="field">
          <label class="block text-900 font-medium mb-2">Пароль</label>
          <Password v-model="registerForm.password" class="w-full custom-password" required toggleMask :feedback="true"/>
        </div>
        <div class="field">
          <label class="block text-900 font-medium mb-2">Повторите пароль</label>
          <Password v-model="registerForm.passwordConfirm" class="w-full custom-password" required toggleMask :feedback="false"/>
        </div>

        <Button label="Далее: Заполнить профиль" class="w-full mt-3" type="submit" :loading="loading"/>
        <div class="text-center mt-3">
          <a @click="switchToLogin" class="text-primary cursor-pointer">
            Уже есть аккаунт? Войти
          </a>
        </div>
      </form>

      <Message v-if="errorMessage" severity="error" :closable="false" class="mt-3">{{ errorMessage }}</Message>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import api from '../utils/api';

import InputText from 'primevue/inputtext';
import Password from 'primevue/password';
import Button from 'primevue/button';
import Message from 'primevue/message';

const router = useRouter();
const viewMode = ref('login');
const loading = ref(false);
const errorMessage = ref('');

const loginForm = ref({
  username: '',
  password: ''
});

const registerForm = ref({
  username: '',
  email: '',
  password: '',
  passwordConfirm: ''
});

const switchToLogin = () => {
  viewMode.value = 'login';
  errorMessage.value = '';
  loginForm.value = { username: '', password: '' };
  registerForm.value = { username: '', email: '', password: '', passwordConfirm: '' };
};

const switchToRegister = () => {
  viewMode.value = 'register';
  errorMessage.value = '';
  loginForm.value = { username: '', password: '' };
  registerForm.value = { username: '', email: '', password: '', passwordConfirm: '' };
};

const handleApiError = (error) => {
  loading.value = false;
  console.error('API Error:', error);
  if (error.response) {
    console.error('Error data:', error.response.data);
    const errorData = error.response.data;
    if (typeof errorData === 'object' && errorData !== null) {
      errorMessage.value = Object.entries(errorData).map(([key, value]) => {
        if (key === 'non_field_errors') return Array.isArray(value) ? value.join(', ') : value;
        return `${key}: ${Array.isArray(value) ? value.join(' ') : value}`;
      }).join('\n');
    } else if (errorData.detail) {
      errorMessage.value = errorData.detail;
    } else {
      errorMessage.value = `Ошибка сервера (${error.response.status})`;
    }
  } else if (error.request) {
    errorMessage.value = 'Сервер не отвечает. Проверьте подключение.';
  } else {
    errorMessage.value = error.message || 'Произошла неизвестная ошибка.';
  }
};

const submitLogin = async () => {
  loading.value = true;
  errorMessage.value = '';
  try {
    const response = await api.post('/auth/jwt/create/', {
      username: loginForm.value.username,
      password: loginForm.value.password
    });
    const { access, refresh } = response.data;
    localStorage.setItem('accessToken', access);
    localStorage.setItem('refreshToken', refresh);
    router.push('/');
  } catch (error) {
    handleApiError(error);
  } finally {
    loading.value = false;
  }
};

const submitRegistrationStep1 = async () => {
  errorMessage.value = '';

  if (registerForm.value.password !== registerForm.value.passwordConfirm) {
    errorMessage.value = 'Пароли не совпадают.';
    return;
  }

  loading.value = true;

  try {
    const registrationPayload = {
      username: registerForm.value.username,
      email: registerForm.value.email,
      password: registerForm.value.password
    };
    await api.post('/auth/users/', registrationPayload);

    try {
      const loginResponse = await api.post('/auth/jwt/create/', {
        username: registerForm.value.username,
        password: registerForm.value.password
      });
      const { access, refresh } = loginResponse.data;
      localStorage.setItem('accessToken', access);
      localStorage.setItem('refreshToken', refresh);
      router.push('/complete-profile');

    } catch (loginError) {
      console.error("Ошибка авто-логина после регистрации:", loginError);
      errorMessage.value = "Регистрация успешна, но не удалось автоматически войти. Пожалуйста, войдите вручную.";
      viewMode.value = 'login';
    }

  } catch (registrationError) {
    handleApiError(registrationError);
  } finally {
    loading.value = false;
  }
};

</script>

<style scoped>
.custom-password :deep(.p-password-input) {
  width: 100%;
}
</style>