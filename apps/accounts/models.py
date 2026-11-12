from io import BytesIO

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.files.base import ContentFile
from django.db import models
from PIL import Image

from apps.fanfics.models import Fanfic

PROFILE_PHOTO_MAX_SIZE = (1000, 1000)


class Notification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="notifications",
        db_index=True,
        on_delete=models.CASCADE,
    )
    verb = models.CharField(max_length=255)
    target_ct = models.ForeignKey(
        ContentType,
        blank=True,
        null=True,
        related_name="target_obj",
        on_delete=models.CASCADE,
    )
    target_id = models.PositiveIntegerField(blank=True, null=True, db_index=True)
    read = models.BooleanField(default=False)
    target = GenericForeignKey("target_ct", "target_id")
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ("-created",)
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"

    def __str__(self):
        return f"{self.user} - {self.verb}"

    def mark_as_read(self):
        self.read = True
        self.save(update_fields=["read"])


class AccountProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="accountprofile",
    )
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to="users/%Y/%m/%d", blank=True, null=True)
    location = models.CharField(max_length=30, blank=True)
    bio = models.TextField(blank=True)
    reco_consent_given = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Account profile"
        verbose_name_plural = "Accounts profiles"

    def __str__(self):
        return f"Profile for user {self.user}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.photo and self._shrink_photo():
            super().save(update_fields=["photo"])

    def _shrink_photo(self) -> bool:
        """Downscale photos wider than 1000px. Returns True when the file changed."""
        with Image.open(self.photo) as photo:
            if photo.width <= PROFILE_PHOTO_MAX_SIZE[0]:
                return False
            photo.thumbnail(PROFILE_PHOTO_MAX_SIZE, Image.Resampling.LANCZOS)
            buffer = BytesIO()
            photo.convert("RGB").save(buffer, format="JPEG", quality=90, optimize=True)
        self.photo.save(self.photo.name, ContentFile(buffer.getvalue()), save=False)
        return True


class Social(models.Model):
    SOCIAL_TYPES = (
        ("twitter", "Twitter"),
        ("facebook", "Facebook"),
        ("pinterest", "Pinterest"),
        ("instagram", "Instagram"),
    )
    network = models.CharField(max_length=255, choices=SOCIAL_TYPES)
    nichandle = models.CharField(max_length=255)
    account = models.ForeignKey(
        AccountProfile,
        related_name="social_network",
        on_delete=models.CASCADE,
        db_index=True,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_index=True
    )

    class Meta:
        ordering = ("network",)
        verbose_name = "Social account"
        verbose_name_plural = "Social accounts"
        unique_together = ("network", "account")

    def __str__(self):
        return f"Social network {self.network} for user {self.user}"


class FollowUser(models.Model):
    user_from = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="rel_from_set",
        on_delete=models.CASCADE,
        db_index=True,
    )
    user_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="rel_to_set",
        on_delete=models.CASCADE,
        db_index=True,
    )
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ("-created",)
        verbose_name = "follow user"
        verbose_name_plural = "follow users"
        unique_together = ("user_from", "user_to")

    def __str__(self):
        return f"{self.user_from} follows {self.user_to}"


class FollowStories(models.Model):
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="fanfic",
        on_delete=models.CASCADE,
        db_index=True,
    )
    to_fanfic = models.ForeignKey(
        Fanfic, related_name="users", on_delete=models.CASCADE, db_index=True
    )
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ("-created",)
        verbose_name = "follow story"
        verbose_name_plural = "follow stories"
        unique_together = ("from_user", "to_fanfic")

    def __str__(self):
        return f"{self.from_user} follows {self.to_fanfic}"
