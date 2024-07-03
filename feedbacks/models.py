from django.db import models
from classify_news.models import ClassifyNews
from accounts.models import User

class Feedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    news_id = models.ForeignKey(ClassifyNews, on_delete=models.CASCADE)
    score = models.IntegerField()
    content = models.CharField(max_length=500)
    create_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)
    delete_at = models.DateField(null=True)



