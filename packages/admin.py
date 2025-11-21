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

for i in _all:
    admin.site.register(i)