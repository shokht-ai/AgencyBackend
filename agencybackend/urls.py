"""
URL configuration for agencybackend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import RegisterView, TokenRefreshFromCookieView, CustomLoginAPIView, LogoutView
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('packages/', include('packages.urls'), name='packages'),
    path('user/', include('userProfile.urls'), name='userprofile'),
    path('purchase-travelers/', include('booking_transaction.urls'), name='purchase-travelers'),

    # Ro‘yxatdan o‘tish
    path('api/register/', RegisterView.as_view(), name='register'),
    # Login (JWT token olish)
    path('api/login/', CustomLoginAPIView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshFromCookieView.as_view(), name='token_refresh'),
    path('api/logout/', LogoutView.as_view(), name='logout')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)