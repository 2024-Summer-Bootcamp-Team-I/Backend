from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserIdParameterSerializer, ScrapedNewsCreateSerializer, ScrapedNewsSerializer
from .models import ScrapedNews
from accounts.models import User
from news.models import News

from drf_yasg.utils import swagger_auto_schema

class ScrapsAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="스크랩 뉴스 전체 조회",

        query_serializer=UserIdParameterSerializer,
        responses={200: ScrapedNewsSerializer(many=True)},
    )
    def get(self, request):
        user_id = request.query_params.get('user_id')
        user = get_object_or_404(User, pk = user_id)
        scraps = ScrapedNews.objects.filter(user_id = user, is_deleted = False)
        serializer = ScrapedNewsSerializer(scraps, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    @swagger_auto_schema(
        operation_summary="뉴스 스크랩",
        query_serializer=UserIdParameterSerializer,
        request_body=ScrapedNewsCreateSerializer,
        responses={201: ScrapedNewsSerializer(), 400: 'Bad Request'}
    )
    def post(self, request):
        # 시리얼라이저로 쿼리 파라미터 검증
        query_serializer = UserIdParameterSerializer(data=request.query_params)
        if not query_serializer.is_valid():
            return Response(query_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user_id = query_serializer.validated_data.get('user_id')
        user = get_object_or_404(User, pk=user_id)
        url = request.data.get('url')

        # 뉴스 존재 여부 확인
        news = get_object_or_404(News, url=url)
        
        # 데이터 유효성 검사 및 생성
        serializer = ScrapedNewsCreateSerializer(data=request.data)
        if serializer.is_valid():
            scraped_news = ScrapedNews.objects.create(user_id=user, news_id=news)
            response_serializer = ScrapedNewsSerializer(scraped_news)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        


class ScrapAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="뉴스 스크랩 취소",
        query_serializer=UserIdParameterSerializer,
        responses={status.HTTP_204_NO_CONTENT: '뉴스 없다. 잘 삭제함'},
    )
    def delete(self, request, news_id):
        user_id = request.query_params.get('user_id')
        user = get_object_or_404(User, pk = user_id)
        scraped_news = ScrapedNews.objects.filter(news_id = news_id, user_id = user, is_deleted = False).first()
        if not scraped_news:
            return Response({"detail": "뉴스가 없어요"}, status=status.HTTP_404_NOT_FOUND)
        scraped_news.is_deleted = True
        scraped_news.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
