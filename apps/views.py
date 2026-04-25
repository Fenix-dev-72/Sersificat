from random import randint

from drf_spectacular.utils import extend_schema
from redis import Redis
from rest_framework import status, request, viewsets
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from apps.models import User, Category, Product, Advertisement, UserAddress
from apps.serializers import UserModelSerializer, EmailVerifySerializer, VerifyOtpCodeSerializer, \
    CategoryModelSerializer, ProductModelSerializer, AdvertisementModelSerializer, ProfileModelSerializer, \
    UserAddressSerializer
from apps.untils import send_email


# Create your views here.

@extend_schema(tags=['Auth'])
class RegisterAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer

class VerifyEmailAPIView(APIView):
    @extend_schema(tags=['Auth'], request=EmailVerifySerializer)
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email kiritilishi shart!'}, status=status.HTTP_400_BAD_REQUEST)
        code = str(randint(10 ** 5, 10 ** 6))
        send_email(email, code)

        # Redis bilan ishlash
        redis_client = Redis(password='1')
        redis_client.mset({f"{email}_code": code})
        redis_client.expire(f"{email}_code", 60)

        return Response({'message': 'Tasdiqlash kodi yuborildi!'}, status=status.HTTP_200_OK)

class VerifyOtpAPIView(APIView):
    @extend_schema(tags=['Auth'], request=VerifyOtpCodeSerializer)
    def post(self, request):
        serializer = VerifyOtpCodeSerializer(data=request.data)

        if serializer.is_valid():
            # Agar bu yerga kelsa, demak kod Serializerda tekshirildi va to'g'ri
            return Response({'message': "OTP kod tasdiqlandi"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DashboardAPIView(APIView):
    def get(self, request): # noqa
        category_id = request.query_params.get('category_id')
        categories = Category.objects.all()
        products = Product.objects.filter(is_active=True).all()
        advertisement = Advertisement.objects.all()
        if category_id:
            products = products.filter(category_id=category_id)

        category_serializer = CategoryModelSerializer(categories, many=True)
        product_serializer = ProductModelSerializer(products, many=True)
        advertisement_serializer = AdvertisementModelSerializer(advertisement,many=True)
        return Response({'categories': category_serializer.data,
                         'products': product_serializer.data,
                         'advertisement': advertisement_serializer.data})


class ProductDetailAPIView(RetrieveAPIView):
    model = Product
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    lookup_field = 'id'


class ProfileRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = ProfileModelSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

class LocationViewSet(ModelViewSet):
    queryset = UserAddress.objects.all()
    serializer_class = UserAddressSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
