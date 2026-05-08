from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager

from django.db.models import Model, CharField, ImageField,TextChoices, DecimalField, ForeignKey, CASCADE

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

