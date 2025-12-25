from django.contrib import admin
from .models import Booking, BookingStatus, PurchaseCustomerInformation, Country, PurchaseTravelersInformation, PurchasePayment, OrderRequest

_all = [
    Booking,
    BookingStatus,
    PurchaseCustomerInformation,
    PurchaseTravelersInformation,
    PurchasePayment,
    OrderRequest,
    Country
]
admin.site.register(_all)
