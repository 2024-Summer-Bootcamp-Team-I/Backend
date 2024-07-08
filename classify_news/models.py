from django.db import models
from news.models import News
from accounts.models import User

class ClassifyNews(models.Model):
    news_id = models.OneToOneField(News, on_delete=models.CASCADE, primary_key=True)
    score = models.IntegerField()
    reason = models.CharField(500)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    deleted_at = models.DateField(null=True)


