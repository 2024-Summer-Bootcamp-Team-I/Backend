from django.urls import path
from .views import save_channel_APIView, channel_score_save_APIView, channel_score_all_APIView, channel_score_APIView

urlpatterns = [
    path('', save_channel_APIView.as_view()),
    path('save/<int:id>', channel_score_save_APIView.as_view()),
    path('scores', channel_score_all_APIView.as_view()),
    path('<int:channel_id>/score',channel_score_APIView.as_view()),
]
