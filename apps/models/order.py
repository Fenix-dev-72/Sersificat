from django.db.models import (Model, CharField, ImageField, TextField,
                              DecimalField, ForeignKey, CASCADE, BooleanField, TimeField, TextChoices, DateTimeField)

from apps.models import User, UserAddress, Product


class Order(Model):
    class StatusChoice(TextChoices):
        New = 'New'
        PENDING = 'pending', 'Kutilmoqda'
        PROCESSING = 'processing', 'Jarayonda'
        SHIPPED = 'shipped', "Yo'lda"
        DELIVERED = 'delivered', 'Yetkazib berildi'
        CANCELLED = 'cancelled', 'Bekor qilindi'

    user = ForeignKey(User, on_delete=CASCADE)
    address = ForeignKey(UserAddress, on_delete=CASCADE, null=True, blank=True)
    created_at = DateTimeField(auto_now_add=True)
    status = CharField(choices=StatusChoice, default=StatusChoice.New, max_length=25)

class OrderItem(Model):
    order = ForeignKey(Order,on_delete=CASCADE)
    product = ForeignKey(Product,on_delete=CASCADE)
    price = DecimalField(max_digits=10, decimal_places=0)
    quantity = DecimalField(max_digits=10, decimal_places=0)
    product_size = CharField(max_length=255)
    product_color = CharField(max_length=255, null=True, blank=True)


