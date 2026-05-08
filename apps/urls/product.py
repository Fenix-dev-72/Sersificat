from django.urls import path

from apps.views import ProductListAPIView, LikeProductListAPIVew, LikeProductAPIView, ProductDetailAPIView, \
    ProductColorListAPIView, ProductSizeListAPIView

urlpatterns = [
    path('products/', ProductListAPIView.as_view()),
    path('products/likes/', LikeProductListAPIVew.as_view()),
    path('procduct/like/<int:pk>', LikeProductAPIView.as_view()),
    path('product/detail/<int:id>/', ProductDetailAPIView.as_view()),
    path('product-colors/',ProductColorListAPIView.as_view()),
    path('product-size/',ProductSizeListAPIView.as_view()),
]