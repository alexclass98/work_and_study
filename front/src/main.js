// main.js

import { createApp } from 'vue';
import App from './App.vue';
import PrimeVue from 'primevue/config';
import router from './router';

// Сервисы
import ToastService from 'primevue/toastservice'; // <-- 1. Импортируйте сервис

import Button from 'primevue/button';
import InputText from 'primevue/inputtext';
import Menubar from 'primevue/menubar';
import Password from 'primevue/password';

// Стили
import 'primevue/resources/themes/saga-green/theme.css'; // Тема
import 'primevue/resources/primevue.min.css';         // Основные стили
import 'primeicons/primeicons.css';                   // Иконки
import 'primeflex/primeflex.css';                     // Утилиты

const app = createApp(App);

app.use(PrimeVue);
app.use(router);
app.use(ToastService);

// Глобальная регистрация компонентов (опционально, можно и локально)
app.component('Button', Button);
app.component('InputText', InputText);
app.component('Menubar', Menubar);
app.component('Password', Password);

app.mount('#app');