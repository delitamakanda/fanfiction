from celery import shared_task
from fanfics.services import compute_recommendations
from django.core.cache import cache
from django.contrib.auth import get_user_model

from fanfics.models import Recommendation

import logging

logger = logging.getLogger(__name__)

User = get_user_model()

@shared_task
def refresh_recos_for_all_users():
	users = User.objects.filter(accountprofile__reco_consent_given=True).exclude(accountprofile__isnull=True)
	for user in users:
		recs = compute_recommendations(user.id)
		fanfic_ids = [rec['id'] for rec in recs]

		cache.set(f"recs_{user.id}", recs, timeout=3600)

		rec_obj, _ = Recommendation.objects.update_or_create(user=user)
		rec_obj.fanfictions.set(fanfic_ids)
		logger.info(f"Refreshing recommendations for user {user.id}")


@shared_task
def purge_recs_from_opted_out_users():
	users = User.objects.filter(accountprofile__reco_consent_given=False).exclude(accountprofile__isnull=True)
	for user in users:
		Recommendation.objects.filter(user=user).delete()
		cache.delete(f"recs_{user.id}")
		logger.info(f"Purging recommendations for user {user.id}")

