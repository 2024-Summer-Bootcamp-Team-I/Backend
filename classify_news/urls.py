from django.urls import path
from .views import ClassifiesAPIView, ClassifyCAPIView

urlpatterns = [
    path("", ClassifiesAPIView.as_view()),
    path("C/<int:news_id>", ClassifyCAPIView.as_view()),
]

