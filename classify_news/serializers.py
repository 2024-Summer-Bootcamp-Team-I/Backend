from rest_framework import serializers
from .models import ClassifyNews

class ClassifyNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassifyNews
        fields = '__all__'

class ClassifyNewsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassifyNews
        fields = ("")