from django.urls import path

from .views import ClassifiesAPIView, ClassifyCAPIView, SNUEmbeddingAPIView, SNUClassifyAPIView

urlpatterns = [
    path("", ClassifiesAPIView.as_view()),
    path("C/<int:news_id>", ClassifyCAPIView.as_view()),
    path("snu/embedding", SNUEmbeddingAPIView.as_view()),
    path("snu/classify", SNUClassifyAPIView.as_view()),
]

