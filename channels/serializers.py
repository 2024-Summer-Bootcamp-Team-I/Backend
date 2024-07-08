from rest_framework import serializers
from .models import Channel, ChannelScore
from classify_news.models import ClassifyNews, News

class CorrectResponse_Serializer(serializers.Serializer):
    message = serializers.CharField()

class Classify_News_Score_Serializer(serializers.ModelSerializer):
    class Meta:
        model = ClassifyNews
        fields = ['score']

class News_for_classify_Serializer(serializers.ModelSerializer):
    classifynews_score = Classify_News_Score_Serializer(source='classifynews', read_only=True)

    class Meta:
        model = News
        fields = ['classifynews_score']

class Channel_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = '__all__'