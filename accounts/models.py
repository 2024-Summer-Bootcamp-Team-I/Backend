from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    nickname = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.username
