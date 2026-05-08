from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from apps.models import Order, OrderItem
from apps.serializers import (OrderModelSerializer, OrderItemsModelSerializer,
                              OrderItemQuantityUpdateModelSerializer)


@extend_schema(tags=['Order'])
class OrderListAPIView(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderModelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('orderitem_set__product__product_images')

@extend_schema(tags=['Order'])
class OrderItemCreateAPIView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderItemsModelSerializer
    permission_classes = [IsAuthenticated]

@extend_schema(tags=['Order'])
class OrderItemQuantityUpdateAPIView(UpdateAPIView):
    http_method_names = ['patch','post']
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemQuantityUpdateModelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return OrderItem.objects.filter(order__user=self.request.user)

@extend_schema(tags=['Order'])
class OrderItemDeleteAPIView(DestroyAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemsModelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return OrderItem.objects.filter(order__user=self.request.user)

@extend_schema(tags=['Order'])
class OrderDeleteAPIView(DestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderModelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)



