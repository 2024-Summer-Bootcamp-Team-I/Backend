from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_yasg.utils import swagger_auto_schema

from .models import User
from .serializers import UserSerializer, LoginResponseSerializer, SigninResponseSerializer, LoginSerializer

class SignupAPIView(APIView):
    @swagger_auto_schema(operation_summary="회원가입", request_body=UserSerializer, responses={"201":SigninResponseSerializer})
    def post(self, request):
        print(__name__)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user_name = serializer.validated_data.get('user_name')

            if User.objects.filter(user_name=user_name).exists():
                return Response({"이미 존재하는 회원입니다."}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({"회원가입이 완료되었습니다."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    @swagger_auto_schema(operation_summary="로그인", request_body=LoginSerializer, responses={"201":LoginResponseSerializer})
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user_name = serializer.validated_data.get('user_name')
            password = serializer.validated_data.get('password')
            if User.objects.filter(user_name=user_name, password=password).exists():
                user = User.objects.get(user_name=user_name)
                return Response({'message': '로그인 되었습니다.'}, status=status.HTTP_200_OK)
            return Response({'message': '아이디 또는 비밀번호가 잘못되었습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)