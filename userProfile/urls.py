from django.urls import path
from .views import (
    UserProfileView, UserAvatarView,
    BookingView, FavoriteView, NotificationView
)

urlpatterns = [
    path("profile/", UserProfileView.as_view()),

    path("avatar/", UserAvatarView.as_view()),

    path("booking/", BookingView.as_view()),
    path("booking/<int:pk>/", BookingView.as_view()),

    path("favorite/", FavoriteView.as_view()),
    path("favorite/<int:pk>/", FavoriteView.as_view()),

    path("notification/", NotificationView.as_view()),
    path("notification/<int:pk>/", NotificationView.as_view()),
]
