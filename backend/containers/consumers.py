import json
from channels.generic.websocket import AsyncWebsocketConsumer

class LogConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Foydalanuvchi ulanganda ishlaydi"""
        self.container_id = self.scope['url_route']['kwargs']['container_id']
        self.room_group_name = f"log_{self.container_id}"

        # Ulanishni qabul qilish
        await self.accept()

        # Test xabar yuborish
        await self.send(text_data=json.dumps({
            'message': f"Ulanish muvaffaqiyatli! Container ID: {self.container_id}"
        }))

    async def disconnect(self, close_code):
        """Foydalanuvchi chiqib ketganda"""
        pass

    async def receive(self, text_data):
        """Foydalanuvchidan xabar kelsa (agar kerak bo'lsa)"""
        pass


