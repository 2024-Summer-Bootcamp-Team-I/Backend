from django.db import models

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    nickname = models.CharField(max_length=20)
    name = models.CharField(max_length=10)
    create_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)
    delete_at = models.DateField(null=True)