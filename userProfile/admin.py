from django.contrib import admin
from .models import *

# Register your models here.

_all = [
    UserProfile,
    UserAvatar,
    Booking,
    BookingStatus,
    Favorite,
    Notification,
    NotificationStatus
]

for i in _all:
    admin.site.register(i)
