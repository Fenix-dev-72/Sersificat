from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from apps.models import ProductImage, ProductComment, Product, ProductLike, ProductValue, ProductColor, \
    ProductSize

class ProductLikeModelSerializer(ModelSerializer):
    class Meta:
        model = ProductLike
        fields = ('id', 'product_id', 'user_id', 'is_active')

class ProductImagesSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('id', 'image','color_id','is_active')

class ProductCommentSerializer(ModelSerializer):
    user = serializers.CharField(source='user.username',read_only=True)
    class Meta:
        model = ProductComment
        fields = ('id', 'product_id', 'comment', 'user',)


class ProductColorSerializer(ModelSerializer):
    class Meta:
        model = ProductColor
        fields = ('id','name','color')

class ProductSizeSerializer(ModelSerializer):
    class Meta:
        model = ProductSize
        fields = ('id','name')

class ProductValueSerializer(ModelSerializer):
    class Meta:
        model = ProductValue
        fields = ('id','product_id','size','price','quantity','characteristics')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['size'] = instance.size.name
        return representation

class ProductModelSerializer(ModelSerializer):
    image = ProductImagesSerializer(source='product_images',many=True, read_only=True)
    comments = ProductCommentSerializer(source='productcomment_set', many=True, read_only=True)
    variants = ProductValueSerializer(source='productvalue_set', many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'description','is_active',
                  'subcategory_id','image','comments','variants','brand',)

    def get_active_images(self, obj): # noqa
        images = obj.product_images.filter(is_active=True)
        return ProductImagesSerializer(images, many=True).data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['subcategory_id'] = instance.subcategory.name
        return representation
