from rest_framework.serializers import ModelSerializer
from apps.models import Category, CubCategory, Catalogue

class SubCategoryModelSerializer(ModelSerializer):
    class Meta:
        model = CubCategory
        fields = ('id', 'name', 'is_active_dashboard', 'image',)


class CategoryModelSerializer(ModelSerializer):
    sub_categories = SubCategoryModelSerializer(source='cubcategory_set',many=True,read_only=True)
    class Meta:
        model = Category
        fields = ('id', 'name', 'catalogue_id', 'sub_categories')


class CatalogModelSerializer(ModelSerializer):
    categories = CategoryModelSerializer(source='category_set',many=True,read_only=True)
    class Meta:
        model = Catalogue
        fields = ('id', 'name', 'Icon','categories',)

