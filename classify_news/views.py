from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ClassifyNews
from news.models import News
from .serializers import ClassifyNewsSerializer, ClassifyNewsCreateSerializer, ClassifyNewsUpdateSerializer, PageParameterSerializer
from drf_yasg.utils import swagger_auto_schema
from .sentiment import analyze_sentiment, recommend_similar_articles
from channels.models import Channel

class ClassifiesAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="판별된 뉴스 전체 조회",
        query_serializer=PageParameterSerializer,
        responses={200: ClassifyNewsSerializer()},
    )
    def get(self, request):
        page = request.query_params.get('page')
        if page is None:
            page = 1
        classifies = ClassifyNews.objects.all()
        paginator = Paginator(classifies, 9)
        page_obj = paginator.get_page(page)
        serializer = ClassifyNewsSerializer(page_obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    @swagger_auto_schema(
        operation_summary="뉴스 판별",
        request_body=ClassifyNewsCreateSerializer,
        responses={201: ClassifyNewsCreateSerializer()},
    )
    def post(self, request):
        serializer = ClassifyNewsCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"기사를 판별했습니다"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClassifyCAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="C",
        responses={200: ClassifyNewsSerializer()},
    )
    def get(self, request, news_id):
        news = get_object_or_404(News, news_id=news_id)
        classify = get_object_or_404(ClassifyNews, news_id=news_id)
        if news.type == 'c':
            serializer = ClassifyNewsSerializer(classify)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Type is not 'c'"}, status=status.HTTP_400_BAD_REQUEST)



class ClassifyAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="A",
        responses={200: ClassifyNewsSerializer()},
    )
    def get(self, request, news_id):
        classify = get_object_or_404(ClassifyNews, news_id=news_id)
        
        news = classify.news_id
        target_article = news.content

        target_score, target_magnitude = analyze_sentiment(target_article)
        articles = list(News.objects.all())
        article_index = articles.index(news)
        recommendations = recommend_similar_articles(article_index, articles)
        
        similar_articles = []
        opposite_articles = []
        
        for similar_news, score in recommendations:
            similar_score, similar_magnitude = analyze_sentiment(similar_news.content)
            channel = get_object_or_404(Channel, id=similar_news.channel_id)
            channel_name = channel.name
            article_data = {
                "news_id": similar_news.news_id,
                "channel": channel_name,
                "title": similar_news.title,
                "url": similar_news.url,
                "similarity": score,
                "sentiment_score": similar_score,
                "sentiment_magnitude": similar_magnitude
            }
            if score > 0.1:
                if (target_score < 0 and similar_score > 0) or (target_score > 0 and similar_score < 0):
                    opposite_articles.append(article_data)
                similar_articles.append(article_data)
        channel = get_object_or_404(Channel, id=news.channel_id)
        channel_name = channel.name
        response_data = {
            "target_article": {
                "title": news.title,
                "content": news.content,
                "channel": channel_name,
                "img":news.img,
                "url": news.url,
                "summarize":news.summarize,
                "published_date":news.published_date,
                "sentiment_score": target_score,
                "sentiment_magnitude": target_magnitude
            },
            "similar_articles": similar_articles,
            "opposite_articles": opposite_articles   
        }
        
        return Response(response_data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="뉴스 재판별",
        request_body=ClassifyNewsUpdateSerializer,
        responses={201: ClassifyNewsUpdateSerializer()},
    )
    def put(self, request, news_id):
        classify = get_object_or_404(ClassifyNews, news_id = news_id)
        serializer = ClassifyNewsUpdateSerializer(classify,data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"기사 판별이 업데이트 되었습니다."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)