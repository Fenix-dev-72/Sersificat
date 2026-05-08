from django.urls import path, include
from drf_spectacular.utils import extend_schema
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.views import CatalogueListAPIView, CategoryListApiView, CubCategoryListApiView

urlpatterns = [
    path('catalogues/', CatalogueListAPIView.as_view()),
    path('categories/', CategoryListApiView.as_view()),
    path('subcategories/', CubCategoryListApiView.as_view()),
]
