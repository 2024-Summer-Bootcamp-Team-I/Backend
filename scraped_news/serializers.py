from rest_framework import serializers
from .models import ScrapedNews
from news.serializers import news_data_Serializer

class ScrapedNewsSerializer(serializers.ModelSerializer):
    news = news_data_Serializer(source='news_id', read_only=True)
    class Meta:
        model = ScrapedNews
        fields = ("news", "user_id", "created_at","updated_at","is_deleted")

class ScrapedNewsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrapedNews
        fields = ("news_id",)

class UserIdParameterSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
