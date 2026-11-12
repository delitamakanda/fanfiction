import logging

from celery import shared_task
from django.contrib.auth import get_user_model

from apps.fanfics import services

logger = logging.getLogger(__name__)


# Explicit names: they are stored in django-celery-beat's periodic tasks.
@shared_task(name="fanfics.tasks.refresh_recos_for_all_users")
def refresh_recos_for_all_users() -> int:
    users = get_user_model().objects.filter(accountprofile__reco_consent_given=True)
    count = 0
    for user in users.iterator():
        services.refresh_recommendations(user)
        count += 1
    logger.info("Recommendations refreshed for %s users", count)
    return count


@shared_task(name="fanfics.tasks.purge_recs_from_opted_out_users")
def purge_recs_from_opted_out_users() -> int:
    users = get_user_model().objects.filter(accountprofile__reco_consent_given=False)
    count = 0
    for user in users.iterator():
        services.clear_recommendations(user)
        count += 1
    logger.info("Recommendations purged for %s users", count)
    return count
