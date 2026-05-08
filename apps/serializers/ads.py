from rest_framework.serializers import ModelSerializer

from apps.models import Advertisement


class AdvertisementModelSerializer(ModelSerializer):
    class Meta:
        model = Advertisement
        fields = ('category', 'image')