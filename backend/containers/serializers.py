from rest_framework import serializers
from .models import Container

class ContainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Container
        fields = ['id', 'name', 'image', 'host_port', 'container_port', 'status', 'created_at']
        read_only_fields = ['id', 'status', 'created_at', 'container_id']

    def validate_host_port(self, value):
        """Port band emasligini tekshirish kerak (keyinchalik)"""
        if value < 1024 or value > 65535:
            raise serializers.ValidationError("Port 1024 va 65535 oralig'ida bo'lishi kerak.")
        return value