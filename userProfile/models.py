from django.db import models
from django.contrib.auth.models import User
from packages.models import Tour
from cryptography_modelFiled import EncryptedField
from booking_transaction.models import Country


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

class UserBankCardInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customer_bankcard_info")
    card_number = EncryptedField(max_length=200, null=True, blank=True)
    card_owner = EncryptedField(max_length=100, null=True, blank=True)
    card_validity_period = EncryptedField(max_length=100, null=True, blank=True)
    card_cvv = EncryptedField(max_length=100, null=True, blank=True)

class UserPassportInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="passport_info")
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, related_name="passport_info")
    passport_full_name = EncryptedField(max_length=100)
    passport_number = EncryptedField(max_length=200)
    birth_date = models.DateField(null=True)

# ============================
# User Profile
# ============================
class UserAvatar(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='avatar')
    avatar = models.ImageField(upload_to='avatar/')

    def __str__(self):
        return str(self.user)




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

    def __str__(self):
        return self.name


# ============================
# Notifications
# ============================
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    notif_type = models.ForeignKey(NotificationStatus, on_delete=models.SET_NULL, null=True,
                                   related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.notif_type}"
