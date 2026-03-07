from channels.generic.websocket import AsyncWebsocketConsumer
import json

class AIConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("ai_group", self.channel_name)
        await self.accept()
    async def receive(self, text_data=None, bytes_data=None):
        print("Received:", text_data)
        await self.send(text_data=json.dumps({"status": "ok"}))
    async def ai_message(self, event):
        await self.send(json.dumps(event["data"]))
