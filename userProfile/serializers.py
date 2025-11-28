from rest_framework import serializers
from django.contrib.auth.models import User

from .models import UserProfile, UserAvatar, Booking, Favorite, Notification  # BookingStatus, NotifacationStatus
from packages.serializers import TourBookingSerializer
from packages.models import Tour


# ============================
# User Serializer (read only)
# ============================
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email"]
        read_only_fields = ['username']


# ============================
# User Profile
# ============================
class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)

    class Meta:
        model = UserProfile
        fields = ["id", "user", "phone", "birth_date", "address"]

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
            "date", "guests", "price", "booking_date", "rating"
        ]
        read_only_fields = ["booking_date"]

class BookingListSerializer(serializers.ModelSerializer):
    tour = TourBookingSerializer(read_only=True)
    status = serializers.CharField(source='status.name')
    class Meta:
        model = Booking
        fields = [
            "id", "tour", "status",
            "date", "guests", "price", "booking_date", "rating"
        ]
    #
    # def get_tour(self, obj):
    #     print(obj, "11")
    #     tour_objs = Tour.objects.get(id=obj)




# ============================
# Favorite
# ============================
class FavoriteTourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = ['id', 'title', 'location', 'rating', 'price']

class FavoriteSerializer(serializers.ModelSerializer):
    tour = FavoriteTourSerializer()
    class Meta:
        model = Favorite
        fields = ["id", "tour", "created_at"]
        read_only_fields = ["created_at"]


# ============================
# Notification
# ============================
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["id", "user", "notif_type", "title", "message", "created_at", "read"]
        read_only_fields = ["created_at"]
