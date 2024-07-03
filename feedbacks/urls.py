from django.urls import path
from .views import FeedbacksAPIView

urlpatterns = [
    path("", FeedbacksAPIView.as_view()),
]