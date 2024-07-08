from django.urls import path

from .views import ScrapsAPIView, ScrapAPIView

urlpatterns = [
    path("", ScrapsAPIView.as_view()),
    path("<int:news_id>/", ScrapAPIView.as_view()),
]
