import json
from channels.generic.websocket import AsyncWebsocketConsumer

class WallConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("wall", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("wall", self.channel_name)

    async def receive(self, text_data):
        message = json.loads(text_data)
        await self.channel_layer.group_send(
            "wall",
            {
                "type": "wall.message",
                "message": message
            }
        )

    async def wall_message(self, event):
        await self.send(text_data=json.dumps(event["message"]))