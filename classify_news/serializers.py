from rest_framework import serializers
from .models import ClassifyNews
from news.serializers import news_data_Serializer

class ClassifyNewsSerializer(serializers.ModelSerializer):
    news = news_data_Serializer(source='news_id', read_only=True)
    channel_name = serializers.SerializerMethodField()
    class Meta:
        model = ClassifyNews
        fields = ("news", "channel_name", "score", "reason", "created_at","updated_at","is_deleted")

    def get_channel_name(self, obj):
        return obj.news_id.channel.name

class ClassifyNewsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassifyNews
        fields = ("news_id","score", "reason")

class ClassifyNewsUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassifyNews
        fields = ("score", "reason")

class SNUCrawlingSerializer(serializers.ModelSerializer):
    url = serializers.URLField()
    snu_num = serializers.IntegerField()
    class Meta:
        model = ClassifyNews
        fields = ['url', 'snu_num']

class SNUClassifySerializer(serializers.ModelSerializer):
    url = serializers.URLField()
    class Meta:
        model = ClassifyNews
        fields = ['url']

class PageParameterSerializer(serializers.Serializer):
    page = serializers.IntegerField()
