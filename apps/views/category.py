from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView
from apps.models import Catalogue, Category, CubCategory
from apps.serializers import CategoryModelSerializer, CatalogModelSerializer, SubCategoryModelSerializer

@extend_schema(tags=['category'])
class CatalogueListAPIView(ListAPIView):
    queryset = Catalogue.objects.all().prefetch_related('category_set')
    serializer_class = CatalogModelSerializer

@extend_schema(tags=['category'])
class CategoryListApiView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer

@extend_schema(tags=['category'])
class CubCategoryListApiView(ListAPIView):
    queryset = CubCategory.objects.all()
    serializer_class = SubCategoryModelSerializer