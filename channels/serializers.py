from rest_framework import serializers
from .models import Channel

class Channel_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = '__all__'

class correctrespones_Serializer(serializers.Serializer):
    message = serializers.CharField()