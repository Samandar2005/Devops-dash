from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Qo'shimcha maydonlar (keyinchalik kerak bo'ladi)
    bio = models.TextField(blank=True, null=True)
    avatar = models.URLField(blank=True, null=True)
    
    # Kelajakda Team/Role qo'shish oson bo'ladi
    is_devops = models.BooleanField(default=False)

    def __str__(self):
        return self.username