from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Feedback
from accounts.models import User
from classify_news.models import ClassifyNews
from .serializers import UserIdParameterSerializer
from .serializers import FeedbackSerializer, FeedbackCreateSerializer

from drf_yasg.utils import swagger_auto_schema

class FeedbacksAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="특정 뉴스의 피드백 조회",
        responses={200: FeedbackSerializer(many=True)},
    )
    def get(self, request, news_id):
        classify_news = get_object_or_404(ClassifyNews, news_id = news_id)
        feedbacks = classify_news.feedback_set.all()
        serializer = FeedbackSerializer(feedbacks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_summary="특정 뉴스의 피드백 생성",
        request_body=FeedbackCreateSerializer,
        query_serializer=UserIdParameterSerializer,
        responses={201: FeedbackCreateSerializer()},
    )
    def post(self, request, news_id):
        user_id = request.query_params.get('user_id')
        user = get_object_or_404(User, user_id = user_id)
        try:
            feedback = Feedback.objects.get(user_id=user_id)
            return Response({"detail": "이미 피드백을 입력한 유저"}, status=status.HTTP_400_BAD_REQUEST)
        except Feedback.DoesNotExist:
            pass
        classify_news = get_object_or_404(ClassifyNews, news_id = news_id)
        serializer = FeedbackCreateSerializer(data=request.data)
        if serializer.is_valid():
            feedback = serializer.save(news_id=classify_news, user_id=user)
            feedback.save()
            return Response({"message":"피드백이 생성되었습니다."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    