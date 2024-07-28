from django.urls import path

from .views import ScrapsAPIView, ScrapAPIView, SearchScrapsAPIView

urlpatterns = [
    path("", ScrapsAPIView.as_view()),
    path("<int:news_id>/", ScrapAPIView.as_view()),
    path("search/", SearchScrapsAPIView.as_view()),
]
