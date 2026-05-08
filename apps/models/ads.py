from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import MinValueValidator
from decimal import Decimal

from django.db.models import Model, ImageField, ForeignKey, CASCADE

from apps.models import CubCategory


#====================REKLAMA===============

class Advertisement(Model):
    category = ForeignKey(CubCategory,on_delete=CASCADE)
    image = ImageField(upload_to='advertisements/')