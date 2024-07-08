from rest_framework import serializers
from .models import News

class news_data_Serializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'

