from django.db import models
from channels.models import Channel

class News(models.Model):
    news_id = models.AutoField(primary_key=True)
    channel = models.ForeignKey(Channel, related_name='news', on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=100)
    content = models.TextField()
    url = models.URLField(null=True)
    category = models.CharField(max_length=20)
    img = models.TextField(default="image")
    published_date = models.CharField()
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
