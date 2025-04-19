# 🎓 SkillUp Platform

**Интерактивная обучающая платформа для оценки и улучшения профессиональных навыков через тестирование и общение.**

[![Language Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://www.python.org/)
[![Framework Django](https://img.shields.io/badge/Framework-Django-0C3C26.svg?logo=django)](https://www.djangoproject.com/)
[![Library Django Channels](https://img.shields.io/badge/Backend-Channels-0C3C26.svg?logo=django)](https://channels.readthedocs.io/)
[![Server Daphne](https://img.shields.io/badge/Server-Daphne-44AE8F.svg)](https://github.com/django/daphne)
[![Language JavaScript](https://img.shields.io/badge/Language-JavaScript-yellow.svg?logo=javascript)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![Framework Vue.js](https://img.shields.io/badge/Framework-Vue.js-4FC08D.svg?logo=vue.js)](https://vuejs.org/)
[![License MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

![image](https://github.com/user-attachments/assets/263cf883-9667-427f-9133-9b1097523be2)


## ✨ Ключевые Особенности

*   **Система Тестирования:**
    *   Прохождение профессиональных тестов для оценки уровня знаний.
    *   Интеграция тестов из внешних источников через `<iframe>`.
    *   (Опционально) Отслеживание результатов и прогресса пользователя.
    *   (Опционально) Подбор тестов на основе профиля или интересов пользователя.
*   **Стена (Общий Чат):**
    *   Страница "Стена" с **real-time** чатом для всех зарегистрированных пользователей.
    *   Обмен сообщениями в реальном времени благодаря **WebSocket** (Django Channels + Daphne).
    *   Возможность видеть сообщения от других пользователей без перезагрузки страницы.
*   **Пользовательские Профили:**
    *   Регистрация и аутентификация пользователей.
    *   (Опционально) Отображение информации о пользователе, пройденных тестах, достижениях.
*   **Панель Управления (Админка Django):**
    *   Управление пользователями, тестами (если они хранятся в БД), настройками платформы.

## 🛠️ Технологический Стек

*   **Бэкенд:**
    *   Python 3.9+
    *   Django 4+
    *   Django REST Framework (DRF) (для API)
    *   Django Channels (для WebSocket)
    *   Daphne (ASGI сервер для Channels)
    *   (Опционально) PostgreSQL / MySQL / SQLite
    *   (Опционально) Redis (как Channel Layer Backend для Channels в продакшене)
*   **Фронтенд:**
    *   JavaScript (ES6+)
    *   Vue.js 3
    *   Vue Router
    *   Pinia
    *   Axios (для HTTP запросов)
    *   WebSocket клиент
    *   Primevue
*   **Инструменты:**
    *   Node.js & npm/yarn
    *   Git & GitHub
