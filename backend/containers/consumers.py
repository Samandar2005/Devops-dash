import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from utils.docker_client import DockerManager

class LogConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # 1. Ulanishni qabul qilish
        await self.accept()
        
        # 2. URL dan Container ID ni olish
        self.container_id = self.scope['url_route']['kwargs']['container_id']
        self.keep_running = True # Loopni boshqarish uchun bayroq

        # 3. Loglarni o'qishni alohida "Task" sifatida fonda boshlaymiz
        self.log_task = asyncio.create_task(self.stream_logs())

    async def disconnect(self, close_code):
        # Ulanish uzilganda log o'qishni to'xtatamiz
        self.keep_running = False
        # Agar task ishlab turgan bo'lsa, uni bekor qilamiz
        if hasattr(self, 'log_task'):
            self.log_task.cancel()

    async def stream_logs(self):
        """Asosiy logika: Docker loglarini bloklamasdan o'qish"""
        docker_manager = DockerManager()
        
        # Bu yerda Docker bilan ulanamiz (Sinxron operatsiya)
        # run_in_executor yordamida uni threadga otamiz
        loop = asyncio.get_running_loop()
        container = await loop.run_in_executor(None, docker_manager.get_container, self.container_id)

        if not container:
            await self.send(text_data=json.dumps({"error": "Container topilmadi"}))
            await self.close()
            return

        # Docker log stream (Sinxron generator)
        # follow=True -> jonli kuzatish (xuddi 'docker logs -f' kabi)
        # tail=50 -> oxirgi 50 qatorni olish
        log_iterator = container.logs(stream=True, follow=True, tail=50)

        # Sinxron iteratorni o'qishni Thread-ga topshiramiz
        await loop.run_in_executor(None, self._read_logs_sync, log_iterator)

    def _read_logs_sync(self, iterator):
        """Bu funksiya alohida thread-da ishlaydi va asosiy serverni qotirmaydi"""
        try:
            for line in iterator:
                if not self.keep_running:
                    break
                
                # Log bayt formatida keladi, uni string qilamiz
                log_text = line.decode('utf-8').strip()
                
                if log_text:
                    # WebSocketga xabar yuborish
                    # Thread ichidan turib Async funksiyani chaqirish uchun 'run_coroutine_threadsafe' kerak
                    asyncio.run_coroutine_threadsafe(
                        self.send(text_data=json.dumps({'log': log_text})),
                        asyncio.get_event_loop()
                    )
        except Exception as e:
            print(f"Log stream error: {e}")


