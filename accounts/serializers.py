from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_name', 'password','nickname','name']


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_name','password']

class LoginResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    user_id = serializers.IntegerField()

class SigninResponseSerializer(serializers.Serializer):
    message = serializers.CharField()