from django.core.management.base import BaseCommand
from containers.services import get_all_containers

class Command(BaseCommand):
    help = 'Docker ulanishini test qilish'

    def handle(self, *args, **kwargs):
        self.stdout.write("Docker konteynerlari qidirilmoqda...")
        
        containers = get_all_containers()
        
        if not containers:
            self.stdout.write(self.style.WARNING("Hozircha hech qanday konteyner topilmadi yoki ulanishda xato bor."))
        else:
            self.stdout.write(self.style.SUCCESS(f"Topildi: {len(containers)} ta konteyner."))
            for c in containers:
                self.stdout.write(f"- [{c['id']}] {c['name']} ({c['status']})")