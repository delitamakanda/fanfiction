from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.accounts.models import AccountProfile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, raw=False, **kwargs):
    """Every user gets an ``AccountProfile``."""
    if created and not raw:
        AccountProfile.objects.get_or_create(user=instance)
