from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    profile, created_profile = Profile.objects.get_or_create(
        user=instance,
        defaults={
            "phone": "0000000000"
        }
    )

    # 🔥 SUPER ADMIN FIRST
    if instance.is_superuser:
        profile.role = "admin"

    # 🔹 NORMAL USER DEFAULT
    elif created_profile:
        profile.role = "public"

    profile.save()
