from drf_spectacular.utils import extend_schema
from rest_framework.generics import  ListAPIView
from apps.models import Advertisement
from apps.serializers import AdvertisementModelSerializer

@extend_schema(tags=['advertisement'])
class AdvertisementListAPIView(ListAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementModelSerializer