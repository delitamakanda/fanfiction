"""Business logic of the fanfics app."""

import logging

from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail
from django.db import transaction
from django.db.models import Count, F
from django.template.loader import render_to_string

from apps.fanfics.models import Fanfic, Recommendation, UserFavorite

logger = logging.getLogger(__name__)

RECOMMENDATIONS_CACHE_TIMEOUT = 60 * 60
MAX_RECOMMENDATIONS = 5


def recommendations_cache_key(user_id: int) -> str:
    return f"recs_{user_id}"


# --------------------------------------------------------------------------- #
# Reading statistics
# --------------------------------------------------------------------------- #


def register_view(fanfic: Fanfic, session) -> bool:
    """Count one view per session. Returns True when the counter moved."""
    session_key = f"viewed_fanfic_{fanfic.pk}"
    if session.get(session_key):
        return False
    Fanfic.objects.filter(pk=fanfic.pk).update(views=F("views") + 1)
    fanfic.refresh_from_db(fields=["views"])
    session[session_key] = True
    return True


@transaction.atomic
def set_like(fanfic: Fanfic, user, *, liked: bool) -> Fanfic:
    """Like or unlike ``fanfic`` and keep ``total_likes`` in sync."""
    if liked:
        fanfic.users_like.add(user)
    else:
        fanfic.users_like.remove(user)
    Fanfic.objects.filter(pk=fanfic.pk).update(total_likes=fanfic.users_like.count())
    fanfic.refresh_from_db(fields=["total_likes"])
    return fanfic


# --------------------------------------------------------------------------- #
# E-mails
# --------------------------------------------------------------------------- #


def fanfic_public_url(fanfic: Fanfic) -> str:
    return f"{settings.FRONTEND_URL.rstrip('/')}/fanfics/{fanfic.slug}"


def share_by_email(
    fanfic: Fanfic, *, name: str, email: str, to_email: str, comments: str = ""
) -> None:
    url = fanfic_public_url(fanfic)
    subject = f'{name} ({email}) recommends you reading "{fanfic.title}"'
    message = f'Read "{fanfic.title}" at {url}\n\n{name}\'s comments: {comments}'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [to_email])


def report_to_moderators(fanfic: Fanfic) -> None:
    context = {"fanfic": fanfic}
    send_mail(
        "fanfiction signalee",
        render_to_string("mail/feedback.txt", context),
        settings.DEFAULT_FROM_EMAIL,
        [settings.SERVER_EMAIL],
        html_message=render_to_string("mail/feedback.html", context),
    )


# --------------------------------------------------------------------------- #
# Recommendations ("readers who liked X also liked Y")
# --------------------------------------------------------------------------- #


def compute_recommendations(
    user_id: int, limit: int = MAX_RECOMMENDATIONS
) -> list[dict]:
    favorites = UserFavorite.objects.filter(user_id=user_id).values("fanfiction_id")
    similar_users = (
        UserFavorite.objects.filter(fanfiction_id__in=favorites)
        .exclude(user_id=user_id)
        .values("user_id")
    )
    scored = (
        UserFavorite.objects.filter(user_id__in=similar_users)
        .exclude(fanfiction_id__in=favorites)
        .values("fanfiction_id")
        .annotate(score=Count("fanfiction_id"))
        .order_by("-score")[:limit]
    )
    ids = [row["fanfiction_id"] for row in scored]
    by_id = {
        fanfic["id"]: fanfic
        for fanfic in Fanfic.published.filter(id__in=ids).values(
            "id", "title", "synopsis"
        )
    }
    return [by_id[pk] for pk in ids if pk in by_id]


def refresh_recommendations(user) -> list[dict]:
    recs = compute_recommendations(user.pk)
    cache.set(recommendations_cache_key(user.pk), recs, RECOMMENDATIONS_CACHE_TIMEOUT)
    recommendation, _ = Recommendation.objects.update_or_create(user=user)
    recommendation.fanfictions.set([rec["id"] for rec in recs])
    return recs


def recommended_fanfics(user):
    """Published fanfics recommended to ``user`` (latest computation)."""
    return Fanfic.published.filter(recommendation__user=user).with_related().distinct()


def clear_recommendations(user) -> None:
    Recommendation.objects.filter(user=user).delete()
    cache.delete(recommendations_cache_key(user.pk))
