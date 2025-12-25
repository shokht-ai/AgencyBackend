from django.db import models
from django.contrib.auth.models import User
from packages.models import Tour
from cryptography_modelFiled import EncryptedField


# Booking Status
class BookingStatus(models.Model):
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name


# Booking History
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="bookings")
    status = models.ForeignKey(BookingStatus, on_delete=models.SET_NULL, null=True, related_name='bookings')

    is_self = models.BooleanField(default=True)
    guests = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField()
    booking_date = models.DateField(auto_now_add=True)
    rating = models.FloatField(null=True, blank=True)  # only for completed tours

    def __str__(self):
        return f"{self.user.username} - {self.tour.title}"


class PurchaseCustomerInformation(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="purchase_customer_information")
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    location = models.CharField(max_length=200, null=True, blank=True)
    special_requests = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.full_name}"


class Country(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class PurchaseTravelersInformation(models.Model):
    booking = models.ForeignKey('Booking', on_delete=models.CASCADE, related_name="purchase_travelers_information")
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, related_name="purchase_travelers_information")
    passport_full_name = EncryptedField(max_length=100)
    passport_number = EncryptedField(max_length=200)
    birth_date = models.DateField()  # Sana saqlanadi, uni shifrlashga hojat yo'q


    def __str__(self):
        return f"{self.passport_full_name}"


class PurchasePayment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="purchase_payment")
    card_number = EncryptedField(max_length=200)
    card_owner = EncryptedField(max_length=100)
    card_validity_period = EncryptedField(max_length=100)
    card_cvv = EncryptedField(max_length=100)

    def __str__(self):
        return f"{self.booking.user.username} - {self.booking.tour.title}"


class OrderRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="order_requests")
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="order_requests")
    user_full_name = models.CharField(max_length=100)
    user_email = models.EmailField()
    user_phone = models.CharField(max_length=15)
    additional_user_comment = models.TextField()
