from django.contrib import admin
from .models import *

# Register your models here.

_all = [
    UserProfile,
    UserAvatar,
    Favorite,
    Notification,
    NotificationStatus
]

admin.site.register(_all)
