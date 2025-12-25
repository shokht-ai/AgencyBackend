from django.db import transaction
from rest_framework import serializers
from .models import *
from userProfile.models import UserProfile, UserBankCardInfo
from userProfile.serializers import UserBankCardInfoSerializer


# from drf_writable_nested import WritableNestedModelSerializer


class OrderRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderRequest
        fields = '__all__'


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class PurchasePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchasePayment
        exclude = ('booking',)


class PurchaseCustomerInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseCustomerInformation
        exclude = ('booking',)


class PurchaseTravelersInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseTravelersInformation
        exclude = ('booking',)


class BookingSerializer(serializers.ModelSerializer):
    purchase_customer_information = PurchaseCustomerInformationSerializer(many=True, required=False)
    purchase_travelers_information = PurchaseTravelersInformationSerializer(many=True, required=False)
    purchase_payment = PurchasePaymentSerializer(many=True, required=False)

    class Meta:
        model = Booking
        exclude = ('user',)

    def validate(self, attrs):
        user = self.context['request'].user
        guests = attrs.get('guests')
        is_self = attrs.get('is_self')
        customer_info = attrs.get('purchase_customer_information', [])
        travelers_info = attrs.get('purchase_travelers_information', [])
        payment_info = attrs.get('purchase_payment', [])

        # is_self logikasi
        if is_self:
            if travelers_info:
                raise serializers.ValidationError({
                    "purchase_travelers_information": "Must be empty if is_self is True"
                })
            # Auto-fill customer_info from user profile
            try:
                profile = UserProfile.objects.get(user=user)
            except UserProfile.DoesNotExist:
                raise serializers.ValidationError({"user": "User profile not found."})
            attrs['purchase_customer_information'] = [{
                'full_name': user.get_full_name(),
                'email': user.email,
                'phone': profile.phone or "",
                'location': profile.address or "",
                'special_requests': ''
            }]
            # Auto-fill payment if empty
            if not payment_info:
                try:
                    card = UserBankCardInfo.objects.get(user=user)
                    attrs['purchase_payment'] = [PurchasePaymentSerializer(card).data]
                except UserBankCardInfo.DoesNotExist:
                    raise serializers.ValidationError({"purchase_payment": "Bank card info not found."})
        else:
            # Validate travelers count matches guests
            if guests != len(travelers_info):
                raise serializers.ValidationError({"guests": "Guests count does not match travelers count."})

        # Validate only one customer_info and payment allowed
        if len(attrs.get('purchase_customer_information', [])) > 1:
            raise serializers.ValidationError({"purchase_customer_information": "Only one allowed."})
        if len(attrs.get('purchase_payment', [])) != 1:
            raise serializers.ValidationError({"purchase_payment": "Exactly one object required."})

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        return self._save_booking(validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):
        return self._save_booking(validated_data, instance)

    def _save_booking(self, validated_data, instance=None):
        # Extract nested data
        customer_info_data = validated_data.pop('purchase_customer_information', [])
        travelers_info_data = validated_data.pop('purchase_travelers_information', [])
        payment_data = validated_data.pop('purchase_payment', [])

        user = self.context['request'].user
        validated_data['user'] = user

        if instance:
            # Update main booking
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
        else:
            instance = Booking.objects.create(**validated_data)

        # Customer info
        if customer_info_data:
            PurchaseCustomerInformation.objects.update_or_create(
                booking=instance,
                defaults=customer_info_data[0]
            )
        elif instance.purchase_customer_information.exists():
            instance.purchase_customer_information.all().delete()

        # Travelers info
        instance.purchase_travelers_information.all().delete()
        for traveler in travelers_info_data:
            PurchaseTravelersInformation.objects.create(booking=instance, **traveler)

        # Payment info
        if payment_data:
            PurchasePayment.objects.update_or_create(
                booking=instance,
                defaults=payment_data[0]
            )
        elif instance.purchase_payment.exists():
            instance.purchase_payment.all().delete()

        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Yaratilgan nested obyektlarni ko'rsatish
        if hasattr(instance, 'purchase_customer_information'):
            representation['purchase_customer_information'] = PurchaseCustomerInformationSerializer(
                instance.purchase_customer_information.all(), many=True
            ).data

        if hasattr(instance, 'purchase_travelers_information'):
            representation['purchase_travelers_information'] = PurchaseTravelersInformationSerializer(
                instance.purchase_travelers_information.all(), many=True
            ).data

        if hasattr(instance, 'purchase_payment'):
            representation['purchase_payment'] = PurchasePaymentSerializer(
                instance.purchase_payment.all(), many=True
            ).data

        # Qo'shimcha ma'lumotlar
        representation['user'] = str(instance.user)
        representation['tour'] = str(instance.tour)
        representation['status'] = str(instance.status)

        return representation
