from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Case, When, Value, IntegerField
from django.db import transaction

# from .models import (
#     UserProfile, UserAvatar, Favorite, Notification
# )
# from booking_transaction.models import Booking
from .serializers import *


class UserProfileView(APIView):
    def patch(self, request):
        data = request.data

        # 1. Request bo‘shligini tekshirish
        allowed_fields = {"user_profile", "bank_card", "passport_info"}
        if not data or not allowed_fields.intersection(data.keys()):
            return Response(
                {"detail": "At least one field is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        response_data = {}

        # 2. Hammasini atomic transaction ichida ishlatamiz
        try:
            with transaction.atomic():

                # --- User Profile ---
                profile_data = data.get("user_profile")
                if profile_data is not None:
                    profile = UserProfile.objects.filter(user=request.user).first()
                    if not profile:
                        return Response(
                            {"profile": "User profile not found"},
                            status=status.HTTP_404_NOT_FOUND
                        )

                    serializer = UserProfileSerializer(
                        profile,
                        data=profile_data,
                        partial=True
                    )
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                    response_data["profile"] = "updated"

                # --- Bank Card ---
                card_data = data.get("bank_card")
                if card_data is not None:
                    card_obj, created = UserBankCardInfo.objects.get_or_create(
                        user=request.user
                    )
                    serializer = UserBankCardInfoSerializer(
                        card_obj,
                        data=card_data,
                        partial=True
                    )
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                    response_data["bank_card"] = "created" if created else "updated"

                # --- Passport ---
                passport_data = data.get("passport_info")
                if passport_data is not None:
                    passport_obj, created = UserPassportInfo.objects.get_or_create(
                        user=request.user
                    )
                    serializer = UserPassportInfoSerializer(
                        passport_obj,
                        data=passport_data,
                        partial=True
                    )
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                    response_data["passport"] = "created" if created else "updated"

        except Exception as e:
            # Transaction ichida xato bo‘lsa rollback qilinadi
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {
                "detail": "Updated successfully",
                "result": response_data
            },
            status=status.HTTP_200_OK
        )


    def get(self, request):
        errors = {}

        user_profile = UserProfile.objects.filter(user=request.user).first()
        if not user_profile:
            errors["profile"] = "User profile not found"

        bank_card = UserBankCardInfo.objects.filter(user=request.user).first()
        if not bank_card:
            errors["bank_card"] = "Bank card information not found"

        passport = UserPassportInfo.objects.filter(user=request.user).first()
        if not passport and False:
            errors["passport"] = "Passport information not found"

        if errors:
            return Response(errors, status=status.HTTP_404_NOT_FOUND)

        return Response({
            "profile": UserProfileSerializer(user_profile).data,
            "bank_card": UserBankCardInfoSerializer(bank_card).data,
            "passport": UserPassportInfoSerializer(passport).data
        }, status=status.HTTP_200_OK)


class UserAvatarView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            # Avatar yozuvini olish yoki yaratish
            avatar_obj = UserAvatar.objects.get(user=user_profile)
        except UserProfile.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except UserAvatar.DoesNotExist:
            return Response({"detail": "User avatar image not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserAvatarSerializer(avatar_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if 'avatar' not in request.FILES:
            return Response({"detail": "Avatar fayli yuborilmadi. Iltimos 'avatar' kaliti orqali rasm yuboring."},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Avatar yozuvini olish yoki yaratish
        avatar_obj, created = UserAvatar.objects.get_or_create(user=user_profile)
        serializer = UserAvatarSerializer(avatar_obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": "Avatar muvaffaqiyatli yuklandi" if created else "Avatar muvaffaqiyatli yangilandi."},
            status=status.HTTP_201_CREATED)


class BookingView(APIView):
    def get(self, request):
        try:
            booking_obj = (
                Booking.objects.filter(user=request.user)
                .annotate(
                    status_order=Case(
                        When(status__name="upcoming", then=Value(1)),
                        When(status__name="completed", then=Value(2)),
                        When(status__name="cancelled", then=Value(3)),
                        default=Value(99),  # boshqa holatlar bo'lsa oxiriga tushadi
                        output_field=IntegerField()
                    )
                )
                .order_by("status_order", "-booking_date")
            )
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = BookingListSerializer(booking_obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # def post(self, request):
    #     serializer = BookingSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save(user=request.user)
    #     return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk=None):
        try:
            booking = Booking.objects.get(id=pk, user=request.user)
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = BookingUpdateStatusSerializer(booking, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteView(APIView):
    def get(self, request):
        try:
            favorite_objs = Favorite.objects.filter(user=request.user)
        except Favorite.DoesNotExist:
            return Response({'error': "Favorite objects not fount"}, status=status.HTTP_404_NOT_FOUND)

        serializer = FavoriteListSerializer(favorite_objs, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = FavoriteSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        try:
            fav = Favorite.objects.get(id=pk, user=request.user)
        except Favorite.DoesNotExist:
            return Response({"error": "Favorite not found"}, status=status.HTTP_404_NOT_FOUND)
        fav.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class NotificationView(APIView):
    def patch(self, request):
        notif_ids = request.data.get('ids', [])

        if not isinstance(notif_ids, list):
            return Response({"detail": "ids should be a list"}, status=status.HTTP_400_BAD_REQUEST)

        updated_count = Notification.objects.filter(user=request.user, id__in=notif_ids).update(read=True)
        return Response({"updated": updated_count}, status=status.HTTP_200_OK)

    def get(self, request):
        try:
            notification_objs = Notification.objects.filter(user=request.user).annotate(
                # read=False bo'lsa 0, read=True bo'lsa 1 → 0 birinchi chiqadi
                read_order=Case(
                    When(read=False, then=Value(0)),
                    When(read=True, then=Value(1)),
                    output_field=IntegerField(),
                )
            ).order_by('read_order', '-created_at')
        except Notification.DoesNotExist:
            return Response({"detail": "Notifications not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = NotificationSerializer(notification_objs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
