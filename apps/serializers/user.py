from django.contrib.auth.hashers import make_password
from redis import Redis
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from apps.models import User, UserAddress


#===============================User=======================

class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('password', 'last_name', 'email','username','email')

    def validate_password(self, value): # noqa
        if len(value) <= 8:
            raise ValidationError('Password uzunligi 8 ga teng yoki kata bolishi kerak')
        return make_password(value)

    def validate_email(self, email): # noqa
        redis = Redis(decode_responses=True,password='1')
        verify = redis.mget(email+'_verify')[0]
        if verify != '1':
            raise ValidationError('Tasdiqlanmagan email kiritildi')
        return email

class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress  # Sizning manzil modelingiz nomi
        fields = ('id', 'longitude', 'latitude')

class ProfileModelSerializer(ModelSerializer):
    locations = UserAddressSerializer(many=True, read_only=True, source='address_set')
    class Meta:
        model = User
        fields = ('first_name','last_name',
                  'email','username','user_profile_image',
                  'birthday','phone_number','locations')