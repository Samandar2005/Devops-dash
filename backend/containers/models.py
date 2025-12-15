from django.db import models
from django.conf import settings

class Container(models.Model):
    STATUS_CHOICES = (
        ('running', 'Running'),
        ('stopped', 'Stopped'),
        ('exited', 'Exited'),
        ('created', 'Created'),
    )

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='containers')
    name = models.CharField(max_length=100, help_text="Konteynerga nom (masalan: my-nginx)")
    image = models.CharField(max_length=100, help_text="Docker Image (masalan: nginx:latest)")
    container_id = models.CharField(max_length=64, blank=True, null=True, unique=True)
    host_port = models.IntegerField(help_text="Tashqi port (masalan: 8080)")
    container_port = models.IntegerField(default=80, help_text="Ichki port (masalan: 80)")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.status})"
    
    class Meta:
        ordering = ['-created_at']