from celery import shared_task
from .models import Container
from utils.docker_client import DockerManager

docker_manager = DockerManager()

@shared_task
def create_container_task(container_db_id):
    """
    Bu funksiya orqa fonda (Workerda) ishlaydi.
    """
    try:
        # 1. Bazadan obyektni olamiz
        instance = Container.objects.get(id=container_db_id)
        
        # 2. Statusni yangilaymiz
        instance.status = 'pulling' # Image tortilayotganini bildirish uchun (ixtiyoriy)
        instance.save()

        # 3. Docker SDK ni chaqiramiz
        port_mapping = {instance.container_port: instance.host_port}
        
        container_id = docker_manager.run_container(
            image_name=instance.image,
            container_name=instance.name,
            port_mapping=port_mapping
        )

        if container_id:
            # Muvaffaqiyatli tugadi
            instance.container_id = container_id
            instance.status = 'running'
            instance.save()
            return f"Container {instance.name} started successfully."
        else:
            # Dockerda xato
            instance.status = 'error'
            instance.save()
            return "Failed to start container in Docker."

    except Container.DoesNotExist:
        return "Container DB record not found."
    except Exception as e:
        # Kutilmagan xato bo'lsa ham statusni yangilash kerak
        if 'instance' in locals():
            instance.status = 'error'
            instance.save()
        return f"Error: {str(e)}"