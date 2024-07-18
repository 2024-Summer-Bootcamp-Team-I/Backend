from rest_framework import serializers
from .models import News
from classify_news.models import ClassifyNews


class news_data_Serializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'
class news_score_Serializer(serializers.ModelSerializer):
    classifynews_score = ClassifyNews

class news_count_Serializer(serializers.ModelSerializer):
    news_count = serializers.IntegerField()
    class Meta:
        model = News
        fields = ("news_count", "created_at")

class correctrespones_Serializer(serializers.Serializer):
    message = serializers.CharField()

