from django.urls import path
from .views import save_channel_APIView, channel_score_list_all_APIView, channel_score_APIView

urlpatterns = [
    path('channels', save_channel_APIView.as_view()),
    path('scores', channel_score_list_all_APIView.as_view()),
    path('score/<int:pk>', channel_score_APIView.as_view()),
]
