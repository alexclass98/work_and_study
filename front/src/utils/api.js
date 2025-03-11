import axios from 'axios'

// Создаем экземпляр axios
const api = axios.create({
    baseURL: 'http://127.0.0.1:8000', // Базовый URL вашего бэкенда
})

// Добавляем интерцептор для вставки токена в заголовки
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('accessToken')
    if (token) {
        console.log('Adding token to headers:', token) // Логируем токен
        config.headers.Authorization = `JWT ${token}`
    }
    return config
})

export default api