from redis import Redis
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer, Serializer



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