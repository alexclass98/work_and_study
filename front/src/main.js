import { createApp } from 'vue'
import App from './App.vue'
import PrimeVue from 'primevue/config'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import Menubar from 'primevue/menubar'
import Password from 'primevue/password'
import 'primevue/resources/themes/saga-green/theme.css' // Тема
import 'primevue/resources/primevue.min.css' // Основные стили
import 'primeicons/primeicons.css' // Иконки
import 'primeflex/primeflex.css' // Утилиты
import router from './router'

const app = createApp(App)
app.use(PrimeVue)
app.use(router)

app.component('Button', Button)
app.component('InputText', InputText)
app.component('Menubar', Menubar)
app.component('Password', Password)
app.mount('#app')