from rest_framework import serializers
from django.contrib.auth.models import User
# from django.utils.timesince import timesince
from django.utils import timezone

from .models import UserProfile, UserAvatar, Favorite, Notification, UserBankCardInfo, \
    UserPassportInfo  # , NotifacationStatus
from packages.models import Tour, TourImage
from booking_transaction.models import Booking, BookingStatus, Country
from packages.serializers import TourBookingSerializer
import re


# ============================
# User Serializer (read only)
# ============================
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


# ============================
# User Profile
# ============================
class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False, allow_null=True)

    class Meta:
        model = UserProfile
        fields = ["user", "phone", "birth_date", "address"]

    def update(self, instance, validated_data):
        # USER ma'lumotlari bo‘lsa — alohida ajratamiz
        user_data = validated_data.pop("user", None)

        # Avval profilni update qilamiz
        if validated_data:
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()

        # User modelini update qilish
        if user_data:
            user = instance.user
            for attr, value in user_data.items():
                setattr(user, attr, value)
            user.save()

        return instance


# ============================
# User Bank Card Information
# ============================
class UserBankCardInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBankCardInfo
        exclude = ['user', 'id']

    # ---------------- VALIDATION ----------------

    def validate_card_number(self, value):
        if not value:
            return value

        clean_value = value.replace(" ", "")

        if not clean_value.isdigit():
            raise serializers.ValidationError(
                "Card number must contain only digits"
            )

        if len(clean_value) != 16:
            raise serializers.ValidationError(
                "Card number must be exactly 16 digits"
            )

        return clean_value

    def validate_card_owner(self, value):
        if not value:
            return value

        parts = value.strip().split()

        if len(parts) != 2:
            raise serializers.ValidationError(
                "Card owner must contain first and last name"
            )

        for part in parts:
            if len(part) < 4:
                raise serializers.ValidationError(
                    "Each part of card owner must be at least 4 characters"
                )

        return value

    def validate_card_validity_period(self, value):
        if not value:
            return value

        if not re.fullmatch(r"\d{2}/\d{2}", value):
            raise serializers.ValidationError(
                "Validity period must be in format NN/NN"
            )

        return value

    def validate_card_cvv(self, value):
        if not value:
            return value

        if not value.isdigit():
            raise serializers.ValidationError(
                "CVV must contain only digits"
            )

        if len(value) not in (3, 4):
            raise serializers.ValidationError(
                "CVV must be 3 or 4 digits"
            )

        return value

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # ---- CARD NUMBER ----
        card_number = representation.get("card_number")
        if card_number and len(card_number) >= 8:
            clean = card_number.replace(" ", "")
            masked = (
                    clean[:4]
                    + " **** **** "
                    + clean[-4:]
            )
            representation["card_number"] = masked

        # ---- CARD OWNER ----
        owner = representation.get("card_owner")
        if owner and len(owner) > 6:
            representation["card_owner"] = (
                    owner[:4] + "*" * 10 + owner[-3:]
            )

        # ---- VALIDITY PERIOD ----
        validity = representation.get("card_validity_period")
        if validity:
            representation["card_validity_period"] = "**/**"

        # ---- CVV ----
        cvv = representation.get("card_cvv")
        if cvv:
            representation["card_cvv"] = "*" * len(cvv)

        return representation


# ============================
# User Passport information
# ============================
class UserPassportInfoSerializer(serializers.ModelSerializer):
    country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all())
    class Meta:
        model = UserPassportInfo
        exclude = ['user', 'id']

        # ---------------- FULL NAME ----------------
        def validate_passport_full_name(self, value):
            if not value:
                raise serializers.ValidationError(
                    "Passport full name is required"
                )

            parts = value.strip().split()

            if len(parts) != 2:
                raise serializers.ValidationError(
                    "Passport full name must contain first and last name"
                )

            for part in parts:
                if len(part) < 4:
                    raise serializers.ValidationError(
                        "Each part of passport full name must be at least 4 characters"
                    )

            return value

        # ---------------- PASSPORT NUMBER ----------------
        def validate_passport_number(self, value):
            if not value:
                raise serializers.ValidationError(
                    "Passport number is required"
                )

            value = value.strip().upper()

            if not re.fullmatch(r"[A-Z]{2}\d{7}", value):
                raise serializers.ValidationError(
                    "Passport number must be in format AANNNNNNN (e.g. AB1234567)"
                )

            return value

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        fullname = representation.get('passport_full_name')
        if fullname and len(fullname) > 7:
            masked = f"{fullname[:4]}{'*' * 10}{fullname[-3:]}"
            representation['passport_full_name'] = masked
        passport = representation.get('passport_number')
        if passport and len(passport) > 7:
            masked = f"{'*' * 6}{passport[-3:]}"
            representation['passport_number'] = masked

        return representation


# ============================
# User Avatar
# ============================
class UserAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAvatar
        fields = ["avatar"]


# ============================
# Booking
# ============================
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            "id", "tour", "status",
            "guests", "price", "rating"
        ]


class BookingListSerializer(serializers.ModelSerializer):
    tour = TourBookingSerializer(read_only=True)
    status = serializers.CharField(source='status.name')

    class Meta:
        model = Booking
        fields = [
            "id", "tour", "status",
            "guests", "price", "booking_date", "rating"
        ]


class BookingUpdateStatusSerializer(serializers.ModelSerializer):
    status = serializers.CharField(required=True, allow_blank=False)

    class Meta:
        model = Booking
        fields = ['status']

    def validate_status(self, value):
        # "" yoki None kelsa → null qilamiz
        if value in ["", None]:
            raise serializers.ValidationError("Bosh bo'lishi mumkin emas.")

        # Stringdan BookingStatus obyektini topamiz
        try:
            return BookingStatus.objects.get(name=value)
        except BookingStatus.DoesNotExist:
            raise serializers.ValidationError("Bunday status mavjud emas")

    def update(self, instance, validated_data):
        """
        validate_status status_obj qaytargani uchun,
        validated_data['status'] ichiga obyekt tushadi.
        """
        status_value = validated_data.get("status", None)
        instance.status = status_value
        instance.save()
        return instance


# ============================
# Favorite
# ============================
class FavoriteTourSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Tour
        fields = ['id', 'title', 'location', 'rating', 'price', 'image']

    def get_image(self, obj):
        try:
            img_url = TourImage.objects.filter(tour=obj).first()
        except TourImage.DoesNotExist:
            return ''
        return img_url.url


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ["id", "tour"]

    def validate(self, attrs):
        user = self.context['request'].user  # request dan user olish
        tour = attrs.get('tour')

        # Duplicate favorite mavjudligini tekshirish
        if Favorite.objects.filter(user=user, tour=tour).exists():
            raise serializers.ValidationError({"tour": "Bu tur allaqachon sevimlilarga qo‘shilgan."})

        return attrs


class FavoriteListSerializer(serializers.ModelSerializer):
    tour = FavoriteTourSerializer()

    class Meta:
        model = Favorite
        fields = ['id', 'tour']


# ============================
# Notification
# ============================
class NotificationSerializer(serializers.ModelSerializer):
    # notif_type ning name maydoni
    notif_type = serializers.CharField(source='notif_type.name', read_only=True)
    # yaratilingan vaqtdan hozirgi vaqtgacha soatlarda
    time_since = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ["id", "notif_type", "title", "message", "time_since", "read"]

    def get_time_since(self, obj):
        """
        Hozirgi vaqt va created_at orasidagi farqni soatlarda qaytaradi
        """
        now = timezone.now()
        delta = now - obj.created_at
        seconds = delta.total_seconds()

        minutes = int(seconds // 60)
        hours = int(seconds // 3600)
        days = int(seconds // 86400)
        months = int(days // 30)
        years = int(days // 365)

        if seconds < 60:
            return 'Hozir'
        elif minutes < 60:
            return f"{minutes} minut oldin"
        elif hours < 24:
            return f"{hours} soat oldin"
        elif days < 30:
            return f"{days} kun oldin"
        elif months < 12:
            return f"{months} oy oldin"
        else:
            return f"{years} yil oldin"
