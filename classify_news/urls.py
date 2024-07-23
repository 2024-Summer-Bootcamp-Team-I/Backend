from django.urls import path
from .views import ClassifiesAPIView, ClassifyAPIView, ClassifyCAPIView

urlpatterns = [
    path("", ClassifiesAPIView.as_view()),
    path("A/<int:news_id>", ClassifyAPIView.as_view()),
    path("C/<int:news_id>", ClassifyCAPIView.as_view()),
]

