# signals.py
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile, UserAvatar, NotificationStatus, Notification
from booking_transaction.models import Booking
import uuid


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # username ni unikal generatsiya qilish (UUID qisqargan versiyasi)
        if not instance.username:
            instance.username = f"user_{str(uuid.uuid4())[:8]}"
            instance.save(update_fields=['username'])

        # UserProfile yaratish
        UserProfile.objects.create(user=instance)

@receiver(pre_save, sender=UserAvatar)
def delete_old_avatar(sender, instance, **kwargs):
    if not instance.pk:
        # Yangi obyekt, eski fayl yo'q
        return

    try:
        old_instance = UserAvatar.objects.get(pk=instance.pk)
    except UserAvatar.DoesNotExist:
        return

    old_file = old_instance.avatar
    new_file = instance.avatar

    # Fayl o'zgargan bo'lsa va mavjud bo'lsa → o'chiramiz
    if old_file and old_file != new_file:
        old_file.delete(save=False)

@receiver(post_save, sender=Booking)
def create_booking_notification(sender, instance, created, **kwargs):
    # TODO: Fronend talabiga qarab message textni o'zgartirish kerak. <br> uchun.
    if created:
        try:
            notif_status = NotificationStatus.objects.get(name="Ordering")
        except NotificationStatus.DoesNotExist:
            notif_status = None

        Notification.objects.create(
            user=instance.user,
            notif_type=notif_status,
            title="Yangi buyurtma olindi.",
            message=f"Hurmatli {instance.user.username}, "
                    f"siz {instance.tour.title} safari uchun {instance.guests} ta mehmon bilan "
                    f"{instance.tour.traveling_date} sanasiga buyurtma berdingiz."
        )

