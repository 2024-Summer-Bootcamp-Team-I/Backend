from django.db import models
from news.models import News
from accounts.models import User

class ScrapedNews(models.Model):
    news_id = models.OneToOneField(News, on_delete=models.CASCADE, primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
