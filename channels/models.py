from django.db import models

class Channel(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    name = models.CharField(max_length=10)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

class ChannelScore(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    channel = models.ForeignKey(Channel, related_name='scores', on_delete=models.CASCADE)
    score = models.IntegerField()
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)