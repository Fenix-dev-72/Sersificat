from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import MinValueValidator
from decimal import Decimal

from django.db.models import (Model, CharField, ImageField, TextField, TextChoices, DecimalField, ForeignKey, CASCADE,
                              BooleanField)


# Create your models here.

class User(AbstractUser):
    class RoleChoice(TextChoices):
        ADMIN = 'admin', 'Admin'
        STAFF = 'staff',  'Staff'
        USER = 'user', 'User'
    role = CharField(choices=RoleChoice, default=RoleChoice.USER)
    user_profile_image = ImageField(upload_to='users_images/')
    birthday= CharField(max_length=10, blank=True, null=True)
    phone_number = CharField(max_length=10, blank=True, null=True)

class UserAddress(Model):
    user = ForeignKey(User,on_delete=CASCADE)
    latitude = DecimalField(max_digits=12, decimal_places=9, blank=True, null=True)
    longitude = DecimalField(max_digits=12, decimal_places=9, blank=True, null=True)

class Category(Model):
    name   = CharField(max_length=255)
    image = ImageField(upload_to='categories/',null=True,blank=True)
    is_active_dashboard = BooleanField(default=True)
    emoji  = CharField(
        max_length=10, blank=True, null=True,
        verbose_name="Emoji (Telegram uchun)",
        help_text="Masalan: 👗 🍎 📱"
    )


    @property
    def display_name(self) -> str:
        """Telegram botda: '👗 Kiyim-kechak'"""
        return f"{self.emoji} {self.name}".strip() if self.emoji else self.name

    def __str__(self):
        return self.display_name

    class Meta:
        verbose_name        = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"

class Product(Model):
    name = CharField(max_length=255)
    description = TextField()
    price = DecimalField(max_digits=10, decimal_places=2)
    category = ForeignKey(Category,on_delete=CASCADE)
    is_active = BooleanField(default=True)

class ProductImage(Model):
    product = ForeignKey(Product,on_delete=CASCADE,related_name='product_images')
    image = ImageField(upload_to='products_images/')
    is_active = BooleanField(default=True)

class ProductComment(Model):
    product = ForeignKey(Product,on_delete=CASCADE)
    comment = TextField()
    user = ForeignKey(User,on_delete=CASCADE)

class Advertisement(Model):
    category = ForeignKey(Category,on_delete=CASCADE)
    image = ImageField(upload_to='advertisements/')
