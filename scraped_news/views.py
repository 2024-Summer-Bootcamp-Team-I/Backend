from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserIdParameterSerializer, ScrapedNewsCreateSerializer, ScrapedNewsSerializer
from .models import ScrapedNews
from accounts.models import User
from .models import ScrapedNews
from news.models import News
from classify_news.models import ClassifyNews

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
        responses={201: ScrapedNewsCreateSerializer()},
    )
    def post(self, request):
        user_id = request.query_params.get('user_id')
        user = get_object_or_404(User, pk = user_id)
        url = request.data.get('url')

        news = News.objects.filter(url=url).first()
        if not news:
            return Response({"detail": "url에 해당하는 뉴스가 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        scraped_news = ScrapedNews.objects.filter(news_id=news, is_deleted=True).first()
        if scraped_news:
            scraped_news.is_deleted = False
            serializer = ScrapedNewsSerializer(scraped_news)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        serializer = ScrapedNewsCreateSerializer(data = request.data)
        if serializer.is_valid():
            scraped_news = ScrapedNews.objects.create(user_id=user, news_id=news)
            serializer = ScrapedNewsSerializer(scraped_news)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
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
