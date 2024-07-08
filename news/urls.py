from django.urls import path
from .views import news_APIView, news_list_APIView

urlpatterns = [
    path('', news_APIView.as_view()),
    path('<int:pk>', news_list_APIView.as_view()),

]