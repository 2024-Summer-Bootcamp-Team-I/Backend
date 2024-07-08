from django.db import models
from channels.models import Channel

class News(models.Model):
    news_id = models.AutoField(primary_key=True)
    channel = models.ForeignKey(Channel, related_name='news', on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=50)
    content = models.TextField()
    category = models.CharField(max_length=20)
    published_date = models.DateField()
    is_deleted = models.BooleanField(null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
