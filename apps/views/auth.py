from random import randint
from django.contrib.admin.utils import lookup_field
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from redis import Redis
from rest_framework import status
from rest_framework.generics import CreateAPIView

from rest_framework.response import Response
from rest_framework.views import APIView


from apps.models import User
from apps.serializers import UserModelSerializer, EmailVerifySerializer, VerifyOtpCodeSerializer
from apps.untils import send_email


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