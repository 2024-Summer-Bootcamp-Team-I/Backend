from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from .models import News
from .serializers import news_data_Serializer, correctrespones_Serializer
from .crowling import crawl_all_news, crawl_news
from apscheduler.schedulers.background import BackgroundScheduler

class news_APIView(APIView):
    @swagger_auto_schema(operation_summary="뉴스기사 저장", request_body= news_data_Serializer, responses= {201:correctrespones_Serializer, 400:"입력정보 오류"})
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
        url = request.get('url')
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

def crawl_all_news_job():
    url = 'https://news.naver.com/section/100'
    try:
        crawl_all_news(url)
        print("크롤링 작업 완료")
    except Exception as e:
        print(f"크롤링 중 오류 발생: {e}")
        
scheduler = BackgroundScheduler()
scheduler.add_job(crawl_all_news_job, 'interval', minutes=2) 
scheduler.start()