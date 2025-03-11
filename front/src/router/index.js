import {createRouter, createWebHistory} from 'vue-router'
import Home from '../views/Home.vue'
import Auth from '../views/Auth.vue'
import Profile from '../views/Profile.vue' // Добавляем страницу профиля
import Wall from '../views/Wall.vue'

const routes = [
    {path: '/', component: Home, meta: {requiresAuth: true}},
    {path: '/auth', component: Auth},
    {path: '/profile', component: Profile, meta: {requiresAuth: true}}, // Профиль требует авторизации
    {
        path: '/wall',
        name: 'Wall',
        component: Wall,
        meta: {requiresAuth: true}
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

router.beforeEach((to, from, next) => {
    const isAuthenticated = localStorage.getItem('accessToken')
    if (to.meta.requiresAuth && !isAuthenticated) {
        next('/auth') // Перенаправляем на страницу авторизации
    } else {
        next()
    }
})

export default router