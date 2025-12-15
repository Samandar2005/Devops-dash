import docker
from django.conf import settings

class DockerManager:
    """
    Singleton patternga o'xshash Docker Client boshqaruvchisi.
    Bu klass to'g'ridan-to'g'ri /var/run/docker.sock bilan gaplashadi.
    """
    
    def __init__(self):
        try:
            # Docker Desktop yoki Serverdagi Daemon bilan ulanish
            self.client = docker.from_env()
        except Exception as e:
            print(f"Docker Daemon bilan ulanib bo'lmadi: {e}")
            self.client = None

    def list_containers(self, all=True):
        """Barcha konteynerlarni ro'yxatini qaytaradi"""
        if not self.client:
            return []
        
        containers = self.client.containers.list(all=all)
        results = []
        for c in containers:
            results.append({
                'id': c.short_id,
                'name': c.name,
                'status': c.status, # running, exited, stopped
                'image': c.image.tags[0] if c.image.tags else "unknown",
                'created': c.attrs['Created']
            })
        return results

    def get_container(self, container_id):
        """Bitta konteyner obyektini oladi"""
        try:
            return self.client.containers.get(container_id)
        except docker.errors.NotFound:
            return None

    def start_container(self, container_id):
        c = self.get_container(container_id)
        if c:
            c.start()
            return True
        return False

    def stop_container(self, container_id):
        c = self.get_container(container_id)
        if c:
            c.stop()
            return True
        return False
    
    def run_container(self, image_name, container_name=None, port_mapping=None):
        """
        Yangi konteyner yaratish va ishga tushirish.
        port_mapping: {80: 8080} (Ichki: Tashqi)
        """
        try:
            ports = {}
            if port_mapping:
                # Docker SDK formati: {'80/tcp': 8080}
                for internal, external in port_mapping.items():
                    ports[f'{internal}/tcp'] = external

            container = self.client.containers.run(
                image_name,
                name=container_name,
                ports=ports,
                detach=True # Orqa fonda ishlashi uchun
            )
            return container.short_id
        except Exception as e:
            print(f"Error running container: {e}")
            return None