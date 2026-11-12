"""Business logic of the accounts app (follows, notifications, account lifecycle).

Views call these functions and stay thin; every function can be reused from a
management command, a Celery task or a test.
"""

import logging
from datetime import timedelta

import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage, send_mail
from django.db import IntegrityError, transaction
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)

from apps.accounts.models import FollowStories, FollowUser, Notification
from apps.fanfics.models import Fanfic

logger = logging.getLogger(__name__)

User = get_user_model()

NOTIFICATION_DEDUP_WINDOW = timedelta(seconds=60)
RECAPTCHA_VERIFY_URL = "https://www.google.com/recaptcha/api/siteverify"


# --------------------------------------------------------------------------- #
# Notifications
# --------------------------------------------------------------------------- #


def create_notification(user, verb: str, target=None) -> bool:
    """Record that ``user`` did ``verb`` (on ``target``).

    The same unread notification is not duplicated within a minute. Returns
    ``True`` when a new notification was created.
    """
    lookup = {
        "user": user,
        "verb": verb,
        "read": False,
        "created__gte": timezone.now() - NOTIFICATION_DEDUP_WINDOW,
    }
    if target is not None:
        lookup["target_ct"] = ContentType.objects.get_for_model(target)
        lookup["target_id"] = target.pk
    if Notification.objects.filter(**lookup).exists():
        return False
    Notification.objects.create(user=user, verb=verb, target=target)
    return True


def notifications_for(user):
    """Notifications emitted by the users that ``user`` follows."""
    return (
        Notification.objects.filter(user__rel_to_set__user_from=user)
        .select_related("user", "user__accountprofile", "target_ct")
        .order_by("-created")
    )


# --------------------------------------------------------------------------- #
# Follows
# --------------------------------------------------------------------------- #


@transaction.atomic
def follow_user(user_from, user_to) -> FollowUser:
    if user_from.pk == user_to.pk:
        raise ValidationError("Vous ne pouvez pas vous suivre vous-même.")
    try:
        with transaction.atomic():
            follow = FollowUser.objects.create(user_from=user_from, user_to=user_to)
    except IntegrityError as exc:
        raise ValidationError("You are already following this user.") from exc
    create_notification(user_from, "a commencé à suivre", user_to)
    return follow


def unfollow_user(user_from, user_to) -> None:
    deleted, _ = FollowUser.objects.filter(
        user_from=user_from, user_to=user_to
    ).delete()
    if not deleted:
        raise ValidationError("You are not following this user.")


@transaction.atomic
def follow_story(user, fanfic: Fanfic) -> FollowStories:
    try:
        with transaction.atomic():
            follow = FollowStories.objects.create(from_user=user, to_fanfic=fanfic)
    except IntegrityError as exc:
        raise ValidationError("You are already following this fanfic.") from exc
    create_notification(user, "a commencé à suivre", fanfic)
    return follow


def unfollow_story(user, fanfic: Fanfic) -> None:
    deleted, _ = FollowStories.objects.filter(from_user=user, to_fanfic=fanfic).delete()
    if not deleted:
        raise ValidationError("You are not following this fanfic.")


# --------------------------------------------------------------------------- #
# Tokens & account lifecycle
# --------------------------------------------------------------------------- #


def blacklist_all_tokens(user) -> int:
    """Blacklist every refresh token of ``user``. Returns how many were found."""
    tokens = list(OutstandingToken.objects.filter(user=user))
    for token in tokens:
        BlacklistedToken.objects.get_or_create(token=token)
    return len(tokens)


@transaction.atomic
def deactivate_account(user, *, blacklist_tokens: bool = True) -> int:
    """Soft-delete ``user`` and e-mail a confirmation. Returns blacklisted tokens."""
    blacklisted = blacklist_all_tokens(user) if blacklist_tokens else 0
    user.is_active = False
    user.save(update_fields=["is_active"])
    transaction.on_commit(lambda: _send_deactivation_email(user))
    logger.info("User %s deactivated (%s tokens blacklisted)", user.pk, blacklisted)
    return blacklisted


def _send_deactivation_email(user) -> None:
    context = {
        "username": user.username,
        "email": user.email,
        "deactivation_date": timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    try:
        send_mail(
            "Account deactivation",
            f"Account deactivation - {user.username}",
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            html_message=render_to_string("mail/account_deletion.html", context),
        )
    except Exception:
        logger.exception("Could not send the deactivation e-mail to user %s", user.pk)


def deactivate_inactive_users(days: int) -> int:
    """Deactivate users who have not logged in for ``days`` days."""
    cutoff = timezone.now() - timedelta(days=days)
    return User.objects.filter(is_active=True, last_login__lte=cutoff).update(
        is_active=False
    )


def send_login_reminders(days: int = 14) -> int:
    """E-mail active users who have not logged in for ``days`` days."""
    cutoff = timezone.now() - timedelta(days=days)
    users = User.objects.filter(is_active=True, last_login__lt=cutoff).exclude(email="")
    sent = 0
    for user in users.iterator():
        content = render_to_string(
            "mail/login_reminder.txt", {"username": user.username}
        )
        sent += send_mail(
            "Vous nous manquez... :(",
            content,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=True,
        )
    return sent


# --------------------------------------------------------------------------- #
# Password reset
# --------------------------------------------------------------------------- #


def send_password_reset_email(email: str) -> None:
    """Send a reset link if an active account uses ``email``.

    Nothing tells the caller whether the address exists (no user enumeration).
    """
    user = User.objects.filter(email__iexact=email, is_active=True).first()
    if user is None:
        logger.info("Password reset requested for an unknown e-mail")
        return
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    reset_url = f"{settings.FRONTEND_URL.rstrip('/')}/password-reset/{uid}/{token}/"
    context = {"user": user, "reset_url": reset_url, "uid": uid, "token": token}
    send_mail(
        "Password reset request",
        f"To reset your password, visit this link: {reset_url}",
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=render_to_string(
            "registration/password_reset_email.html", context
        ),
    )
    logger.info("Password reset e-mail sent to user %s", user.pk)


# --------------------------------------------------------------------------- #
# Contact form
# --------------------------------------------------------------------------- #


def verify_recaptcha(token: str) -> bool:
    """Check a reCAPTCHA v3 token with Google."""
    try:
        response = requests.post(
            RECAPTCHA_VERIFY_URL,
            data={"secret": settings.RECAPTCHA_SECRET_KEY, "response": token},
            timeout=5,
        )
        result = response.json()
    except (requests.RequestException, ValueError):
        logger.warning("reCAPTCHA verification failed", exc_info=True)
        return False
    return bool(result.get("success")) and result.get("score", 0) >= (
        settings.RECAPTCHA_MIN_SCORE
    )


def send_contact_message(*, name: str, email: str, subject: str, message: str) -> None:
    """Forward the contact form to the webmaster (``SERVER_EMAIL``).

    The visitor goes in ``Reply-To``: sending *from* their address would fail
    SPF/DMARC checks.
    """
    body = f"De: {name} <{email}>\n\nSujet: {subject}\n\nMessage:\n{message}"
    EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.SERVER_EMAIL],
        reply_to=[email],
    ).send()
