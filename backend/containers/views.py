from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .tasks import create_container_task
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
        # 1. DB ga 'created' statusi bilan saqlaymiz
        instance = serializer.save(owner=self.request.user, status='created')

        # 2. Og'ir ishni Celeryga berib yuboramiz (Async)
        # .delay() metodi vazifani Redis navbatiga tashlaydi
        create_container_task.delay(instance.id)
        
        # 3. Biz kutib o'tirmaymiz, darhol javob qaytamiz!
        
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