from django.db import models
from news.models import News
from accounts.models import User

class ScrapedNews(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    news_id = models.ForeignKey(News, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['news_id', 'user_id'], name='unique_news_user')
        ]
