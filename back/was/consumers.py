# was_app/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async # Для асинхронного доступа к БД
from was_app.serializers import MessagesSerializer, AuthUserSerializer # Нужны для отправки данных
from was_app.models import AuthUser # Нужна модель пользователя

class WallConsumer(AsyncWebsocketConsumer):
    GROUP_NAME = "wall_updates" # Имя группы для рассылки

    async def connect(self):
        # Присоединение к группе при подключении клиента
        await self.channel_layer.group_add(
            self.GROUP_NAME,
            self.channel_name # Уникальное имя канала для этого клиента
        )
        await self.accept() # Принять WebSocket соединение
        print(f"WebSocket connected: {self.channel_name}")

    async def disconnect(self, close_code):
        # Отсоединение от группы при отключении клиента
        await self.channel_layer.group_discard(
            self.GROUP_NAME,
            self.channel_name
        )
        print(f"WebSocket disconnected: {self.channel_name}")

    # Этот метод будет вызван, когда из Django отправляется сообщение в группу
    # с 'type': 'wall.message'
    async def wall_message(self, event):
        message_data = event['message'] # Получаем данные сообщения из события

        # Получаем полные данные автора (асинхронно)
        author_data = await self.get_user_data(message_data.get('author'))

        # Отправляем сообщение клиенту через WebSocket
        await self.send(text_data=json.dumps({
            'type': 'new_message', # Тип события для фронтенда
            'message': message_data,
            'author_details': author_data # Добавляем данные автора
        }))
        print(f"Sent message to {self.channel_name}")

    # Вспомогательная асинхронная функция для получения данных пользователя
    @database_sync_to_async
    def get_user_data(self, user_id):
        if not user_id:
            return None
        try:
            user = AuthUser.objects.get(pk=user_id)
            # Используем существующий сериализатор, убедитесь, что он включает нужные поля
            serializer = AuthUserSerializer(user)
            return serializer.data
        except AuthUser.DoesNotExist:
            return None
