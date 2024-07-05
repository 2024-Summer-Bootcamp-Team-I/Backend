from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from .models import Channel
from .serializers import Channel_Serializer, correctrespones_Serializer

class save_channel_APIView(APIView):
    @swagger_auto_schema(operation_summary="언론사 저장", request_body=Channel_Serializer, responses={201:correctrespones_Serializer, 404:"입력정보 오류"})
    def post(self, request):
        serializer = Channel_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "언론사가 저장되었습니다."}, status = status.HTTP_201_CREATED)
        return Response({"message": "잘못된 접근입니다."}, status = status.HTTP_400_BAD_REQUEST)
        
class channel_score_list_all_APIView(APIView):
    @swagger_auto_schema(operation_summary="언론사 점수 전체조회",responses={200:correctrespones_Serializer, 404:"Not Found"})
    def get(self, request):
        channels = Channel.objects.all()
        serializer = Channel_Serializer(channels, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
       
    
class channel_score_APIView(APIView):
    @swagger_auto_schema(operation_summary="언론사 점수 개별조회",responses={200:correctrespones_Serializer})
    def get(self, request, pk):
        try:
            channel = Channel.objects.get(pk=pk)
        except Channel.DoesNotExist:
            return Response({"message": "해당 언론사를 찾을 수 없습니다."}, status = status.HTTP_404_NOT_FOUND)
        
        serializer = Channel_Serializer(channel)
        return Response(serializer.data, status = status.HTTP_200_OK)
        