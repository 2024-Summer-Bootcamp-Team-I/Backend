from django.db import models

class Channel(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    name = models.CharField(max_length=10)
    score = models.IntegerField(null=False)
    is_deleted = models.BooleanField(null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
