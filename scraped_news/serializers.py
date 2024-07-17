from rest_framework import serializers
from .models import ScrapedNews
from news.serializers import news_data_Serializer

class ScrapedNewsSerializer(serializers.ModelSerializer):
    news = news_data_Serializer(source='news_id', read_only=True)
    channel_name = serializers.SerializerMethodField()
    class Meta:
        model = ScrapedNews
        fields = ("news", "channel_name", "user_id", "created_at","updated_at","is_deleted")

    def get_channel_name(self, obj):
        return obj.news_id.channel.name

class ScrapedNewsCreateSerializer(serializers.ModelSerializer):
    url = serializers.CharField(max_length = 100)
    class Meta:
        model = ScrapedNews
        fields = ("url",)

class UserIdParameterSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
