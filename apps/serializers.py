from django.contrib.auth.hashers import make_password
from redis import Redis
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer, Serializer

from apps.models import User, Category, Product, ProductImage, ProductComment, Advertisement, UserAddress


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('password', 'last_name', 'email',)

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

class VerifyOtpCodeSerializer(Serializer):
    email = CharField(max_length=255)
    code = CharField(max_length=6)

    def validate(self, attrs):
        email = attrs.get('email')
        code = attrs.get('code')

        # decode_responses=True string formatida olish uchun shart
        redis_conn = Redis(host='localhost', port=6379, password='1', decode_responses=True)

        # Kodni olish
        otp_code = redis_conn.get(f"{email}_code")

        if not otp_code:
            raise ValidationError({'error': 'Kodning muddati tugagan'})

        if str(otp_code) != str(code):
            raise ValidationError({'error': 'Kod xato'})

        # Hammasi to'g'ri bo'lsa, vaqtinchalik verify statusini qo'yamiz
        redis_conn.set(f"{email}_verify", "1", ex=120)
        return attrs

class EmailVerifySerializer(Serializer):
    email = CharField(max_length=255)

class CategoryModelSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('id','name','is_active_dashboard','image')



class ProductImagesSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('id', 'image')

class ProductCommentSerializer(ModelSerializer):
    user = serializers.CharField(source='user.username',read_only=True)
    class Meta:
        model = ProductComment
        fields = ('id', 'product_id', 'comment', 'user')

class ProductModelSerializer(ModelSerializer):
    image = ProductImagesSerializer(source='product_images',many=True, read_only=True)
    comments = ProductCommentSerializer(source='productcomment_set', many=True, read_only=True)
    class Meta:
        model = Product
        fields = ('id', 'name', 'description','price',
                  'is_active','category_id','image','comments')

    def get_active_images(self, obj): # noqa
        images = obj.product_images.filter(is_active=True)
        return ProductImagesSerializer(images, many=True).data


class AdvertisementModelSerializer(ModelSerializer):
    class Meta:
        model = Advertisement
        fields = ('category', 'image')


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