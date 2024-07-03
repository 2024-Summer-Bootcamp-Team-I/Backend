from django.db import models
from news.models import News
from accounts.models import User

class ClassifyNews(models.Model):
    news_id = models.OneToOneField(News, on_delete=models.CASCADE, primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    is_fishing = models.BooleanField(default=False)
    is_faked = models.BooleanField(default=False)
    reason = models.CharField(500)
    is_saved = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    deleted_at = models.DateField(null=True)


