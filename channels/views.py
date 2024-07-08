
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from .models import Channel, ChannelScore
from classify_news.models import ClassifyNews, News
from .serializers import Channel_Serializer, CorrectResponse_Serializer
from django.db.models import Avg

class save_channel_APIView(APIView):
    @swagger_auto_schema(operation_summary="언론사 저장", 
                         request_body=Channel_Serializer, 
                         responses={201:CorrectResponse_Serializer, 404:"입력정보 오류"})
    def post(self, request):
        name = request.data.get('name')
        if Channel.objects.filter(name=name).exists():
            return Response({"message": "이미 존재하는 언론사입니다."}, status=status.HTTP_200_OK)

        serializer = Channel_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "언론사가 저장되었습니다."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class channel_score_APIView(APIView):
    @swagger_auto_schema(operation_summary="언론사 점수조회",
                         responses={201:CorrectResponse_Serializer, 404:"입력정보 오류"})
    def post(self, request, id):
        try:
            channel = Channel.objects.get(id=id)
        except Channel.DoesNotExist:
            return Response({"message": "채널이 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        # 특정 Channel과 관련된 News들의 ClassifyNews 점수 평균 계산
        avg_score = ClassifyNews.objects.filter(news_id__channel_id=channel.id).aggregate(average_score=Avg('score'))['average_score']
        
        if avg_score is None:
            return Response({"message": "평균 점수를 계산할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        # ChannelScore 저장 또는 업데이트
        ChannelScore.objects.create(
            channel=channel, 
            score = avg_score
        )

        return Response({"message": "언론사 점수조회.", "score": avg_score}, status=status.HTTP_201_CREATED)

