from django.urls import path
from .views import TourListView

urlpatterns = [
    path('tours/', TourListView.as_view(), name='tour-list'),
]
