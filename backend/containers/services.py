from utils.docker_client import DockerManager

# Global instance (har safar yangi ulanish ochmaslik uchun)
docker_manager = DockerManager()

def get_all_containers():
    """Tizimdagi barcha konteynerlarni olib kelish"""
    return docker_manager.list_containers()

def start_container_service(container_id):
    return docker_manager.start_container(container_id)

def stop_container_service(container_id):
    return docker_manager.stop_container(container_id)