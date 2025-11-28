from datetime import timedelta
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from dotenv import load_dotenv
load_dotenv('../.env')

class CustomLoginAPIView(TokenObtainPairView):
    permission_classes = [AllowAny]

    def post(self, request, **kwargs):
        username = request.data.get("username") #.strip().lower().replace(" ", ".")
        password = request.data.get("password")
        remember_me = request.data.get("remember_me", False)

        # Django ning default authenticate — faqat username orqali ishlaydi
        user = authenticate(request, username=username, password=password)

        if user is None:
            return Response({"detail": "Username yoki parol noto'g'ri"}, status=status.HTTP_401_UNAUTHORIZED)

        # JWT token yaratish
        refresh = RefreshToken.for_user(user)
        lifetime = timedelta(days=30) if remember_me else timedelta(hours=1)
        # Refresh muddati
        refresh.set_exp(lifetime=lifetime)

        access_token = str(refresh.access_token)

        # Javob
        response = Response({
            'access': access_token,
            'user_id': user.pk
        })

        # Refresh token cookie’da
        response.set_cookie(
            key='refresh_token',
            value=str(refresh),
            httponly=True,
            # secure=os.getenv('DEBUG') != 'True',  # production -> True
            secure=False,  # production -> True
            samesite='None',
            max_age=int(lifetime.total_seconds()),
            # path="/api/refresh/"
            path="/"
        )

        return response


class TokenRefreshFromCookieView(APIView):
    """
    Refresh token cookie orqali keladi va yangi access token qaytariladi
    """


    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')

        if not refresh_token:
            return Response({'detail': 'Refresh token mavjud emas.'}, status=status.HTTP_403_FORBIDDEN)

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            return Response({'access': access_token})
        except TokenError:
            response = Response(
                {"detail": "Invalid refresh token"},
                status=status.HTTP_401_UNAUTHORIZED
            )
            response.delete_cookie("refresh_token")
            return response

# --------------------
# Serializer
# --------------------
class RegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password", "email")
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # remember_me ni olib tashlaymiz, chunki User modeli buni qabul qilmaydi
        # validated_data['username'] = validated_data['username'].strip().lower().replace(" ", ".")
        user = User.objects.create_user(**validated_data)
        return user


# --------------------
# View
# --------------------
class RegisterView(generics.CreateAPIView):
    # TODO: requestdan username ko'rinishida orasi _ bilan to'ldirilgan ism-familiya keladi. Bu holatni qayta o'ylab ko'rish kerak.
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

