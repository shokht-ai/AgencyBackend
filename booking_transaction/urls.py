from rest_framework.routers import DefaultRouter
from .views import *
from django.urls import path
router = DefaultRouter()
router.register(r'', PurchaseCustomViewSet, basename='purchase-travelers-information')

urlpatterns = [
    path("countries/", CountryViewSet.as_view({'get': 'list'})),
              ] + router.urls