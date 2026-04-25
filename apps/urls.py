from django.urls import path, include
from drf_spectacular.utils import extend_schema
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.views import RegisterAPIView, VerifyEmailAPIView, VerifyOtpAPIView, DashboardAPIView, ProductDetailAPIView, \
    ProfileRetrieveUpdateAPIView, LocationViewSet

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('login/', extend_schema(tags=['Auth'])(TokenObtainPairView).as_view(), name = 'token_obtain_pair'),
    path('token/refresh/', extend_schema(tags=['Auth'])(TokenRefreshView).as_view(), name='token_refresh'),
    path('verify/email-verify',VerifyEmailAPIView.as_view()),
    path('verify/otp-verify',VerifyOtpAPIView.as_view()),
    path('dashboard/', DashboardAPIView.as_view()),
    path('product/detail/<int:id>/',ProductDetailAPIView.as_view()),
    path('profile/',ProfileRetrieveUpdateAPIView.as_view()),
]

router = DefaultRouter()
router.register(r'location', LocationViewSet)
urlpatterns += router.urls