from django.db import models

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    nickname = models.CharField(max_length=20)
    name = models.CharField(max_length=10)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    is_deleted = models.BooleanField(default=False)