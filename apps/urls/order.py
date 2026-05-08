from django.urls import path

from apps.views import OrderListAPIView, OrderItemCreateAPIView, OrderItemQuantityUpdateAPIView, OrderItemDeleteAPIView, \
    OrderDeleteAPIView

urlpatterns = [
    path('order-create/',OrderItemCreateAPIView.as_view()),
    path('order-list/',OrderListAPIView.as_view()),
    path('update/quantity/<int:pk>/',OrderItemQuantityUpdateAPIView.as_view()),
    path('delete/Item/<int:pk>/',OrderItemDeleteAPIView.as_view()),
    path('order/delete/<int:pk>/',OrderDeleteAPIView.as_view()),
]