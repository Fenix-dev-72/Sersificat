from django.db.models import Min, Max
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.models import Product, ProductLike, ProductColor, ProductSize
from apps.serializers import ProductModelSerializer, ProductLikeModelSerializer, ProductColorSerializer, \
    ProductSizeSerializer

@extend_schema(tags=['product'])
class ProductListAPIView(ListAPIView):
    queryset = Product.objects.annotate( min_price=Min('productvalue__price'),max_price=Max('productvalue__price')).prefetch_related('productvalue_set').all()
    serializer_class = ProductModelSerializer
    filter_backends = (DjangoFilterBackend,SearchFilter,OrderingFilter)
    filterset_fields = ('brand','name','subcategory__name',)
    search_fields = ('name','brand',)
    ordering_fields = ('name','brand','subcategory__name','min_price','max_price',)

@extend_schema(tags=['product'])
class LikeProductListAPIVew(ListAPIView):
    serializer_class = ProductLikeModelSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def get_queryset(self):
        return ProductLike.objects.filter(user=self.request.user,is_active=True)

@extend_schema(tags=['product'])
class LikeProductAPIView(CreateAPIView):
    queryset = ProductLike.objects.all()
    serializer_class = ProductLikeModelSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def perform_create(self, serializer):
        product_id = self.kwargs.get('pk')
        obj, created = ProductLike.objects.get_or_create(product_id=product_id,
                                                         user_id=self.request.user.id,
                                                         defaults={'is_active':True})

        if not created:
            obj.is_active = not obj.is_active
            obj.save()

@extend_schema(tags=['product'])
class ProductDetailAPIView(RetrieveAPIView):
    model = Product
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    lookup_field = 'id'

@extend_schema(tags=['product'])
class ProductColorListAPIView(ListAPIView):
    queryset = ProductColor.objects.all()
    serializer_class = ProductColorSerializer

@extend_schema(tags=['product'])
class ProductSizeListAPIView(ListAPIView):
    queryset = ProductSize.objects.all()
    serializer_class = ProductSizeSerializer

