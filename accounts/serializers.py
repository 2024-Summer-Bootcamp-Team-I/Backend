from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'nickname', 'name')

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError({"password": "비밀번호가 일치하지 않습니다."})

        if User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError({"username": "이미 존재하는 사용자 이름입니다."})

        return attrs

    def create(self, validated_data):
        validated_data.pop('password2') 
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password1'],
            nickname=validated_data['nickname'],
            name=validated_data['name']
        )
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if not username or not password:
            raise serializers.ValidationError({'에러': '아이디와 비밀번호를 입력해주세요'})

        return attrs