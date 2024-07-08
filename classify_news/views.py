from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import ClassifyNews
from news.models import News
from .serializers import ClassifyNewsSerializer, ClassifyNewsCreateSerializer

from drf_yasg.utils import swagger_auto_schema

class ClassifiesAPIView(APIView):
    def get(self, request):
        classifies = ClassifyNews.objects.all()
        serializer = ClassifyNewsSerializer(classifies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request):
        serializer = ClassifyNewsCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"기사를 판별했습니다"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClassifyAPIView(APIView):
    def get(self, request, news_id):
        classify = get_object_or_404(ClassifyNews, news_id = news_id)
        serializer = ClassifyNewsSerializer(classify)
    def put(self, request, news_id):
        classify = get_object_or_404(ClassifyNews, news_id = news_id)
        serializer = ClassifyNewsCreateSerializer(classify,data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"기사 판별이 업데이터 되었습니다."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

