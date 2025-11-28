from django.db import models
from django.contrib.auth.models import User
from packages.models import Tour


# ============================
# User Profile
# ============================
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    phone = models.CharField(max_length=30, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name()


# ============================
# User Profile
# ============================
class UserAvatar(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='avatar')
    avatar = models.ImageField(upload_to='avatar/')


# ============================
# Booking Status
# ============================
class BookingStatus(models.Model):
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name


# ============================
# Booking History
# ============================
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="bookings")
    status = models.ForeignKey(BookingStatus, on_delete=models.SET_NULL, null=True, related_name='bookings')

    date = models.DateField()  # Travel date
    guests = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField()
    booking_date = models.DateField(auto_now_add=True)
    rating = models.FloatField(null=True, blank=True)  # only for completed tours

    def __str__(self):
        return f"{self.user.username} - {self.tour.title}"


# ============================
# Favorite Tours
# ============================
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="favorited_by")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "tour")  # avoid duplicate favorites

    def __str__(self):
        return f"{self.user.username} → {self.tour.title}"


# ============================
# Notification Status
# ============================
class NotificationStatus(models.Model):
    name = models.CharField(max_length=15)


# ============================
# Notifications
# ============================
class Notification(models.Model):
    # NOTIF_TYPES = (
    #     ("booking", "Booking"),
    #     ("promo", "Promo"),
    #     ("reminder", "Reminder"),
    # )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    notif_type = models.ForeignKey(NotificationStatus, on_delete=models.SET_NULL, null=True,
                                   related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.title}"
