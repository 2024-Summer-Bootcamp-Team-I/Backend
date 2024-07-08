from django.urls import path
from .views import save_channel_APIView, channel_score_APIView

urlpatterns = [
    path('', save_channel_APIView.as_view()),
    path('scores/<int:id>', channel_score_APIView.as_view()),
]
