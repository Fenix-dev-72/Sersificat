from django.db.models import (Model, CharField, ImageField, TextField,
                              DecimalField, ForeignKey, CASCADE, BooleanField, SmallIntegerField, JSONField)

from .user import User
from .category import CubCategory


class Product(Model):
    name = CharField(max_length=255)
    description = TextField()
    subcategory = ForeignKey(CubCategory,on_delete=CASCADE)
    brand = CharField(max_length=255)
    is_active = BooleanField(default=True)

class ProductSize(Model):
    name = CharField(max_length=255)

class ProductValue(Model):
    product = ForeignKey(Product,on_delete=CASCADE)
    size = ForeignKey(ProductSize,null=True,blank=True,on_delete=CASCADE)
    price = DecimalField(max_digits=10, decimal_places=0)
    quantity = SmallIntegerField(null=True,blank=True)
    characteristics = JSONField()

class ProductColor(Model):
    name =CharField(max_length=255)
    color = CharField(max_length=255)

class ProductImage(Model):
    product = ForeignKey(Product,on_delete=CASCADE,related_name='product_images')
    image = ImageField(upload_to='products_images/')
    color = ForeignKey(ProductColor,on_delete=CASCADE,related_name='product_images')
    is_active = BooleanField(default=True)

class ProductComment(Model):
    product = ForeignKey(Product,on_delete=CASCADE)
    comment = TextField()
    user = ForeignKey(User,on_delete=CASCADE)

class ProductLike(Model):
    product = ForeignKey(Product,on_delete=CASCADE)
    user = ForeignKey(User,on_delete=CASCADE)
    is_active = BooleanField(default=True)
