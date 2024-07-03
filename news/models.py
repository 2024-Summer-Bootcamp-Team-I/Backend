from django.db import models

class News(models.Model):
    news_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    content = models.TextField()
    category = models.CharField(max_length=20)
    channel = models.CharField(max_length=40)
    published_date = models.DateField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    deleted_at = models.DateField(null=True)
