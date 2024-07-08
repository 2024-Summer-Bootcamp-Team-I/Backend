from rest_framework import serializers
from .models import Channel, ChannelScore

class CorrectResponse_Serializer(serializers.Serializer):
    message = serializers.CharField()

class Channel_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = '__all__'

class ChannelsScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChannelScore
        fields = ['channel_id', 'score']

class ChannelScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChannelScore
        fields = ['created_at', 'score']