from datetime import timedelta
from django.contrib.auth.models import User
from rest_framework import generics, serializers
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.tokens import RefreshToken



class TokenRefreshFromCookieView(APIView):
    """
    Refresh token cookie orqali keladi va yangi access token qaytariladi
    """
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')

        if not refresh_token:
            return Response({'detail': 'Refresh token mavjud emas.'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            return Response({'access': access_token})
        except TokenError:
            return Response({'detail': 'Invalid refresh token'}, status=status.HTTP_401_UNAUTHORIZED)
# --------------------
# Serializer
# --------------------
class RegisterSerializer(ModelSerializer):
    remember_me = serializers.BooleanField()
    class Meta:
        model = User
        fields = ("username", "password", "email", "remember_me")
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # remember_me ni olib tashlaymiz, chunki User modeli buni qabul qilmaydi
        validated_data.pop('remember_me', None)
        user = User.objects.create_user(**validated_data)
        return user

# --------------------
# View
# --------------------
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        remember_me = serializer.is_valid.get('remember_me', False)

        # JWT token yaratish
        refresh = RefreshToken.for_user(user)
        if remember_me:
            refresh.set_exp(lifetime=timedelta(days=30))
        else:
            refresh.set_exp(lifetime=timedelta(hours=1))

        # Access token
        access_token = str(refresh.access_token)

        # Response yaratish va cookie o'rnatish
        response = Response({
            'access': access_token
        })
        response.set_cookie(
            key='refresh_token',
            value=str(refresh),
            httponly=True,           # JS orqali ko'rinmaydi
            secure=False,            # HTTPS bo'lsa True qilishingiz mumkin
            samesite='Lax',
            max_age=30*24*60*60 if remember_me else 3600
        )

        return response
