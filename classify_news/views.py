from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ClassifyNews
from news.models import News
from .serializers import ClassifyNewsSerializer, ClassifyNewsCreateSerializer, ClassifyNewsUpdateSerializer, PageParameterSerializer, SNUCrawlingSerializer, SNUClassifySerializer
from drf_yasg.utils import swagger_auto_schema
from channels.models import Channel
from .snu_save_c_news import crawl_news
from .snu_crawl import snu_crawl
from .snu_embedding import snu_embedding
from .snu_classify_c_news import c_news_classify

class ClassifiesAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="판별된 뉴스 전체 조회",
        query_serializer=PageParameterSerializer,
        responses={200: ClassifyNewsSerializer()},
    )
    def get(self, request):
        page = request.query_params.get('page', 1)
        keyword = request.query_params.get('keyword', '')

        try:
            if keyword:
                classifies = ClassifyNews.objects.filter(
                    Q(news_id__title__icontains=keyword) |
                    Q(news_id__channel__name__icontains=keyword)
                ).order_by('news_id')
            else:
                classifies = ClassifyNews.objects.all().order_by('news_id')

            paginator = Paginator(classifies, 9)
            page_obj = paginator.get_page(page)
            serializer = ClassifyNewsSerializer(page_obj, many=True)
            response_data = {
                'total_pages': paginator.num_pages,
                'results': serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
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
    

class SNUEmbeddingAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="SNU 뉴스 저장 및 검증정보 크롤링(C type)",
        request_body=SNUCrawlingSerializer,
    )
    def post(self, request):
        serializer = SNUCrawlingSerializer(data = request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        url = request.data.get('url')
        snu_num = request.data.get('snu_num')
        try:
            crawl_news(url)
            snu_crawl(snu_num)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"아마": "잘 됐을걸 확인해봐. c-type 뉴스랑 검증정보 txt"}, status=status.HTTP_201_CREATED)
    
    @swagger_auto_schema(
        operation_summary="SNU 검증정보 임베딩",
    )
    def get(self, request):
        try:
            snu_embedding()
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"이거도": "잘 됐을걸 확인해봐. 오픈서치 저장값"}, status=status.HTTP_200_OK)

class SNUClassifyAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="SNU 뉴스 판별 및 저장",
        request_body=SNUClassifySerializer,
    )
    def post(self, request):
        serializer = SNUClassifySerializer(data = request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        url = request.data.get('url')
        news = News.objects.get(url = url)
        news_id = news.news_id
        try:
            c_news_classify(news_id)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return  Response({"진짜" : "잘 됐을걸 확인해봐. 판별뉴스 테이블"}, status=status.HTTP_201_CREATED)




