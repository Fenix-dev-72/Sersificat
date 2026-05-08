from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from apps.models import Order, OrderItem
from apps.serializers import ProductModelSerializer


class OrderItemsModelSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('id','product','price','quantity','product_size','product_color')

    def create(self, validated_data):
        user = self.context['request'].user
        order = Order.objects.filter(user=user,status=Order.StatusChoice.New).first()
        if order:
            validated_data['order'] = order
        else:
            validated_data['order'] = Order.objects.create(user=user,status=Order.StatusChoice.New)

        return super().create(validated_data)

class OrderItemsListSerializer(ModelSerializer):
    product = ProductModelSerializer(read_only=True)
    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'price', 'quantity', 'product_size', 'product_color')



class OrderModelSerializer(ModelSerializer):
    items = OrderItemsListSerializer(source='orderitem_set',read_only=True,many=True)
    class Meta:
        model = Order
        fields = ('id','user','address','status', 'items')


class OrderItemQuantityUpdateModelSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('quantity',)