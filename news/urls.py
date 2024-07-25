from django.urls import path
from .views import news_APIView, news_list_APIView, CrawlNewsView, CountCrawlNewsAPIView, CountClassifyNewsAPIView, NewsTimelineAPIView, AAPIView

urlpatterns = [
    path('', news_APIView.as_view()),
    path('<int:pk>', news_list_APIView.as_view()),
    path('crawlnews',CrawlNewsView.as_view()),
    path('count/crawl', CountCrawlNewsAPIView.as_view()),
    path('count/classify', CountClassifyNewsAPIView.as_view()),
    path('timeline', NewsTimelineAPIView.as_view()),
    path("A/<int:news_id>", AAPIView.as_view()),
]