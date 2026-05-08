from django.urls import path

from apps.views import AdvertisementListAPIView

urlpatterns = [
    path('ads/', AdvertisementListAPIView.as_view()),
]
