from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import ClassifyNews
from news.models import News
from .serializers import ClassifyNewsSerializer, ClassifyNewsCreateSerializer, ClassifyNewsUpdateSerializer, PageParameterSerializer

from drf_yasg.utils import swagger_auto_schema

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

class ClassifyAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="판별된 뉴스 개별 조회",
        responses={200: ClassifyNewsSerializer()},
    )
    def get(self, request, news_id):
        classify = get_object_or_404(ClassifyNews, news_id = news_id)
        serializer = ClassifyNewsSerializer(classify)
        return Response(serializer.data, status=status.HTTP_200_OK)

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

