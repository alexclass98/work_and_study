import axios from 'axios'

const api = axios.create({
    baseURL: 'http://your-django-backend.com/api',
    headers: {
        'Content-Type': 'application/json'
    }
})

api.interceptors.request.use(config => {
    const token = localStorage.getItem('accessToken')
    if (token) {
        config.headers.Authorization = `JWT ${token}`
    }
    return config
})

export default api