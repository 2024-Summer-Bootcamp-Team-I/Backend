from django.db import models
from channels.models import Channel

class News(models.Model):
    news_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    content = models.TextField()
    category = models.CharField(max_length=20)
    channel_id = models.ForeignKey(Channel, related_name='channel_id', on_delete=models.DO_NOTHING)
    published_date = models.DateField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    is_deleted = models.BooleanField(null=True)
