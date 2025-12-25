import uuid
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework import generics, serializers, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken

from dotenv import load_dotenv

load_dotenv('../.env')


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Frontend refresh token cookie'dan yuboradi deb faraz qilamiz
            refresh_token = request.COOKIES.get('refresh_token')
            if refresh_token is None:
                return Response({"detail": "Refresh token topilmadi."},
                                status=status.HTTP_400_BAD_REQUEST)

            # Tokenni obyektga aylantirish
            token = RefreshToken(refresh_token)
            token.blacklist()  # tokenni blacklistga qo‘shish

        except TokenError:
            return Response({"detail": "Invalid token."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Cookie’dan tokenni o‘chirish
        response = Response({"detail": "Siz muvaffaqiyatli logout qilindingiz."},
                            status=status.HTTP_200_OK)
        response.delete_cookie('refresh_token')
        return response


class EmailLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    remember_me = serializers.BooleanField(default=False)


class CustomLoginAPIView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = EmailLoginSerializer  # Custom serializer

    def post(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")
        remember_me = serializer.validated_data.get("remember_me")

        user = authenticate(request, email=email, password=password)

        if user is None:
            return Response({"detail": "Email yoki parol noto'g'ri"}, status=status.HTTP_401_UNAUTHORIZED)
        # login(request, user)
        # JWT token yaratish
        refresh = RefreshToken.for_user(user)
        lifetime = timedelta(days=30) if remember_me else timedelta(hours=1)
        # Refresh muddati
        refresh.set_exp(lifetime=lifetime)

        access_token = str(refresh.access_token)

        # Javob
        response = Response({
            'access': access_token
        })

        # Refresh token cookie’da
        response.set_cookie(
            key='refresh_token',
            value=str(refresh),
            # httponly=True,
            # secure=True,  # production -> True
            # samesite='None',
            max_age=timedelta(days=1),
            expires=(timezone.now() + timedelta(days=1)).strftime('%a, %d-%b-%Y %H:%M:%S GMT'),
            path="/"
        )
        return response


class TokenRefreshFromCookieView(APIView):
    permission_classes = [AllowAny]
    """
    Refresh token cookie orqali keladi va yangi access token qaytariladi
    """

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")
        if not refresh_token:
            return Response({"detail": "Refresh token mavjud emas."}, status=status.HTTP_403_FORBIDDEN)

        try:
            refresh = RefreshToken(refresh_token)
            outstanding = OutstandingToken.objects.get(jti=refresh['jti'])
            BlacklistedToken.objects.get_or_create(token=outstanding)
            refresh.set_jti()
            refresh.set_exp()
            new_refresh_token = str(refresh)  # yangi refresh token
            access_token = str(refresh.access_token)

            response = Response({"access": access_token})
            # Cookie-ga yangi refresh token yozish
            response.set_cookie(
                key="refresh_token",
                value=new_refresh_token,
                # httponly=True,
                # secure=True,
                # samesite="None",
                max_age=timedelta(days=1),
                expires=(timezone.now() + timedelta(days=1)).strftime('%a, %d-%b-%Y %H:%M:%S GMT'),
            )
            print(refresh_token)
            print(new_refresh_token)
            print(refresh_token==new_refresh_token)
            return response

        except TokenError:
            response = Response({"detail": "Invalid refresh token"}, status=status.HTTP_401_UNAUTHORIZED)
            # Cookie-ni o‘chirish
            response.delete_cookie("refresh_token")
            return response


# --------------------
# Serializer
# --------------------
class RegisterSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=True, min_length=6)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'password']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered")
        return value

    def create(self, validated_data):
        phone = validated_data.pop('phone', None)
        password = validated_data.pop('password')
        validated_data['username'] = f"user_{str(uuid.uuid4())[:8]}"
        # User yaratish
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        # UserProfile signal orqali yaratiladi, phone ni update qilish
        if phone:
            profile = user.profile
            profile.phone = phone
            profile.save()

        return user


# --------------------
# View
# --------------------
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
