from django.urls import path
from .views import ClassifiesAPIView, ClassifyAPIView

urlpatterns = [
    path("", ClassifiesAPIView.as_view()),
    path("<int:news_id>", ClassifyAPIView.as_view()),
]
