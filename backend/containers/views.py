from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Container
from .serializers import ContainerSerializer
from utils.docker_client import DockerManager

docker_manager = DockerManager()

class ContainerViewSet(viewsets.ModelViewSet):
    serializer_class = ContainerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Har kim faqat o'zining konteynerlarini ko'radi"""
        return Container.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        """
        1. DB ga yozish.
        2. Docker konteynerni ko'tarish.
        3. Agar Docker o'xshasa, container_id ni DB ga saqlash.
        """
        # Hozircha DB ga saqlab turamiz (Docker hali ishga tushmadi)
        instance = serializer.save(owner=self.request.user, status='created')

        # Docker bilan ishlash
        port_mapping = {instance.container_port: instance.host_port}
        
        container_id = docker_manager.run_container(
            image_name=instance.image,
            container_name=instance.name,
            port_mapping=port_mapping
        )

        if container_id:
            instance.container_id = container_id
            instance.status = 'running'
            instance.save()
        else:
            # Agar Dockerda xato bo'lsa, DB dan ham o'chiramiz (Rollback)
            instance.delete()
            raise serializers.ValidationError({"error": "Docker konteynerini yaratib bo'lmadi. Image nomi to'g'rimi?"})

    @action(detail=True, methods=['post'])
    def stop(self, request, pk=None):
        """Konteynerni to'xtatish"""
        container = self.get_object()
        if docker_manager.stop_container(container.container_id):
            container.status = 'stopped'
            container.save()
            return Response({'status': 'stopped'})
        return Response({'error': 'Failed to stop'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        """Konteynerni qayta ishga tushirish"""
        container = self.get_object()
        if docker_manager.start_container(container.container_id):
            container.status = 'running'
            container.save()
            return Response({'status': 'running'})
        return Response({'error': 'Failed to start'}, status=status.HTTP_400_BAD_REQUEST)