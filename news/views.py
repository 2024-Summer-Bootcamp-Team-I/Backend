from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from .models import News
from scraped_news.models import ScrapedNews
from .serializers import news_data_Serializer, correctrespones_Serializer, news_count_Serializer, similar_news_Serializer, news_url_Serializer
from .crowling import crawl_all_news, crawl_news
from apscheduler.schedulers.background import BackgroundScheduler
from django.db.models import Count, Subquery
from datetime import datetime, timedelta
from django.db.models.functions import RowNumber
from django.db.models import Window, F
from .timeline import get_similar_news_ids
from channels.models import Channel
from django.shortcuts import get_object_or_404
from .sentiment import analyze_sentiment, recommend_similar_articles

class news_APIView(APIView):
    @swagger_auto_schema(operation_summary="뉴진스기사 저장", request_body= news_data_Serializer, responses= {201:correctrespones_Serializer, 400:"입력정보 오류"})
    def post(self, request):
        serializer = news_data_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "뉴스기사가 저장되었습니다."}, status = status.HTTP_201_CREATED)
        return Response({"message": "입력값이 잘못되었습니다."}, status = status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_summary="뉴스기사 전체조회", responses= {200:"조회완료"})
    def get(self, request):
        news_list = News.objects.all()
        serializer = news_data_Serializer(news_list, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)

class news_list_APIView(APIView):
    @swagger_auto_schema(operation_summary="뉴스기사 개별조회",responses={200:correctrespones_Serializer, 404:"Not Found"})
    def get(self, request, pk):
        try:
            news = News.objects.get(pk=pk)
        except News.DoesNotExist:
            return Response({"message": "해당 기사를 찾을 수 없습니다."}, status = status.HTTP_404_NOT_FOUND)
        serializer = news_data_Serializer(news)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
class CrawlNewsView(APIView):
    @swagger_auto_schema(operation_summary="뉴스기사 개별 크롤링", responses= {201:correctrespones_Serializer, 400:"입력정보 오류"})
    def get(self, request, *args, **kwargs):
        url = request.query_params.get('url')
        if not url:
            return Response({"error": "URL parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            news = crawl_news(url)
            return Response({
                "channel_id": news.channel_id,
                "title": news.title,
                "content": news.content,
                "published_date": news.published_date
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CountCrawlNewsAPIView(APIView):
    @swagger_auto_schema(operation_summary="일자별 크롤링 뉴스 개수 조회", responses= {200:news_count_Serializer})
    def get (self, request):
        counts = News.objects.values('created_at').annotate(news_count = Count('news_id')).order_by('-created_at')[:8]
        serializer = news_count_Serializer(counts, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CountClassifyNewsAPIView(APIView):
    @swagger_auto_schema(operation_summary="일자별 판별뉴스(C-type) + 스크랩 개수 조회", responses= {200:news_count_Serializer})
    def get (self, request):
        scrap_counts = ScrapedNews.objects.filter(is_deleted=False).values('created_at').annotate(scrap_count = Count('id')).order_by('-created_at')[:8]
        c_counts = News.objects.filter(type = 'c').values('created_at').annotate(c_count = Count('news_id')).order_by('-created_at')[:8]
        
        scrap_counts_list = list(scrap_counts)
        c_counts_list = list(c_counts)

        combined_counts = {}

        for item in scrap_counts_list:
            date = item['created_at']
            combined_counts[date] = combined_counts.get(date, 0) + item['scrap_count']

        for item in c_counts_list:
            date = item['created_at']
            combined_counts[date] = combined_counts.get(date, 0) + item['c_count']

        combined_counts_list = [{'created_at': date, 'news_count': count} for date, count in combined_counts.items()]
                
        serializer = news_count_Serializer(combined_counts_list, many = True)


        return Response(serializer.data, status=status.HTTP_200_OK)
    

class NewsTimelineAPIView(APIView):
    @swagger_auto_schema(operation_summary="뉴스 타임라인",
        request_body=news_url_Serializer, responses= {200:news_count_Serializer})
    def post (self, request):
        url = request.data.get('url')
        target_news = News.objects.filter(url=url).first()
        target_news_id = target_news.news_id
        target_news_date = target_news.published_date
        start_date = (datetime.strptime(target_news_date[:10], '%Y-%m-%d') - timedelta(days=6)).strftime('%Y-%m-%d')
        end_date = (datetime.strptime(target_news_date[:10], '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')

        similar_news_ids = get_similar_news_ids(target_news_id)
        similar_news = News.objects.filter(
            news_id__in = similar_news_ids, 
            published_date__gte = start_date, 
            published_date__lt = end_date
            ).values('published_date', 'title', 'url').annotate(row_num=Window(
                expression=RowNumber(),
                order_by=F('published_date').desc()
                )).filter(row_num__lte=5).order_by('-published_date')

        serializer = similar_news_Serializer(similar_news, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class AAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="A",
        responses={200: news_data_Serializer()},
    )
    def get(self, request, news_id):
        try:
            classify = get_object_or_404(News, news_id=news_id)
            news = classify.news_id
            target_article = classify.content

            target_score, target_magnitude = analyze_sentiment(target_article)
            articles = list(News.objects.all())

            # Ensure that `news` is in `articles`
            try:
                article_index = next(i for i, article in enumerate(articles) if article.news_id == news_id)
            except ValueError:
                return Response({"detail": "Article not found in the database."}, status=status.HTTP_404_NOT_FOUND)
            
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
            
            channel = get_object_or_404(Channel, id=classify.channel_id)
            channel_name = channel.name
            
            response_data = {
                "target_article": {
                    "title": classify.title,
                    "content": classify.content,
                    "channel": channel_name,
                    "img": classify.img,
                    "url": classify.url,
                    "summarize": classify.summarize,
                    "published_date": classify.published_date,
                    "sentiment_score": target_score,
                    "sentiment_magnitude": target_magnitude
                },
                "similar_articles": similar_articles,
                "opposite_articles": opposite_articles   
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
        
        except Exception as e:
            # Log the exception if needed
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




def crawl_all_news_job():
    url = 'https://news.naver.com/section/105'
    try:
        crawl_all_news(url)
        print("크롤링 작업 완료")
    except Exception as e:
        print(f"크롤링 중 오류 발생: {e}")
        
scheduler = BackgroundScheduler()
scheduler.add_job(crawl_all_news_job, 'interval', minutes=1) 
scheduler.start()