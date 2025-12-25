from django.contrib import admin
from .models import *
# Register your models here.

_all = [
    Category,
    Agency,
    Tour,
    TourImage,
    Highlight,
    IncludedItem,
    NotIncludedItem,
    ItineraryDay,
    ItineraryActivity,
    Facility
]

admin.site.register(_all)