from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.views import ProfileRetrieveUpdateAPIView, LocationViewSet

urlpatterns = [
    path('profile/', ProfileRetrieveUpdateAPIView.as_view()),
]

router = DefaultRouter()
router.register(r'location', LocationViewSet)
urlpatterns += router.urls