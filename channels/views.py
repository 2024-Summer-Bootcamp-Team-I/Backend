from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from .models import Channel, ChannelScore
from classify_news.models import ClassifyNews
from .serializers import CorrectResponse_Serializer, ChannelsScoreSerializer, ChannelScoreSerializer, Channel_name_Serializer
from django.db.models import Avg, Max
from apscheduler.schedulers.background import BackgroundScheduler

class save_channel_APIView(APIView):
    @swagger_auto_schema(operation_summary="언론사 저장", 
                         request_body=Channel_name_Serializer, 
                         responses={201:CorrectResponse_Serializer, 404:"입력정보 오류"})
    def post(self, request):
        name = request.data.get('name')
        if Channel.objects.filter(name=name).exists():
            channel = Channel.objects.get(name=name)
            return Response({"message": "이미 존재하는 언론사입니다.", "id": channel.id}, status=status.HTTP_200_OK)
        
        serializer = Channel_name_Serializer(data=request.data)
        if serializer.is_valid():
            try:
                channel = serializer.save()
                return Response({"message": "언론사가 저장되었습니다.", "id": channel.id}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class channel_score_save_APIView(APIView):
    @swagger_auto_schema(operation_summary="언론사 점수저장",
                         responses={201:CorrectResponse_Serializer, 404:"입력정보 오류"})
    def post(self, request, id):
        try:
            channel = Channel.objects.get(id=id)
        except Channel.DoesNotExist:
            return Response({"message": "채널이 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        avg_score = ClassifyNews.objects.filter(news_id__channel_id=channel.id).aggregate(average_score=Avg('score'))['average_score']
        
        if avg_score is None:
            return Response({"message": "평균 점수를 계산할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        ChannelScore.objects.create(
            channel=channel, 
            score = avg_score
        )
        return Response({"message": "언론사 점수저장.", "score": avg_score}, status=status.HTTP_201_CREATED)
    
class channel_score_all_APIView(APIView):
    @swagger_auto_schema(operation_summary="언론사 점수전체 조회",
                         responses={201:CorrectResponse_Serializer(many=True), 404:"가져오기 실패"})
    def get(self, request):
        recent_channel_scores = ChannelScore.objects.filter(
            id__in = ChannelScore.objects.values('channel').annotate(latest_id=Max('id')).values('latest_id')).order_by('channel_id')

        if not recent_channel_scores.exists():
            return Response({"message": "점수를 가져올 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        # ChannelScore 객체들을 시리얼라이즈합니다.
        serializer = ChannelsScoreSerializer(recent_channel_scores, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

class channel_score_APIView(APIView):
    @swagger_auto_schema(operation_summary="언론사 1개 시간대별 조회",
                         responses={201:CorrectResponse_Serializer(many=True), 404: "가져오기 실패"}
                         )
    def get(self, request, channel_id):
        recent_channel_score = ChannelScore.objects.filter(channel_id=channel_id).all()

        if not recent_channel_score.exists():
            return Response({"message": "점수를 가져올 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ChannelScoreSerializer(recent_channel_score, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

def save_channel_scores():
    channels = Channel.objects.all()
    for channel in channels:
        avg_score = ClassifyNews.objects.filter(news_id__channel_id=channel.id).aggregate(average_score=Avg('score'))['average_score']
        if avg_score is not None:
            ChannelScore.objects.create(
                channel=channel, 
                score=avg_score
            )

scheduler = BackgroundScheduler()
scheduler.add_job(save_channel_scores, 'interval', hours=1) 
scheduler.start()