from rest_framework import serializers
from .models import ClassifyNews
from news.serializers import news_data_Serializer

class ClassifyNewsSerializer(serializers.ModelSerializer):
    news = news_data_Serializer(source='news_id', read_only=True)
    class Meta:
        model = ClassifyNews
        fields = ("news", "score", "reason", "created_at","updated_at","is_deleted")

class ClassifyNewsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassifyNews
        fields = ("news_id","score", "reason")