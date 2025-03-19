from channels.generic.websocket import AsyncWebsocketConsumer
import json


class WallConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Принимаем соединение первым делом
        await self.accept()

        # Подключаемся к группе
        await self.channel_layer.group_add(
            "wall_updates",
            self.channel_name
        )
        print(f"WebSocket connected: {self.channel_name}")

    async def disconnect(self, close_code):
        # Отключаемся от группы
        await self.channel_layer.group_discard(
            "wall_updates",
            self.channel_name
        )
        print(f"WebSocket disconnected: {self.channel_name}")

    async def new_message(self, event):
        # Отправляем сообщение клиенту
        print(f"Sending message: {event['message']}")
        await self.send(text_data=json.dumps(event["message"]))