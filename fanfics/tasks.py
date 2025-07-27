from celery import shared_task
from fanfics.models import Recommendation
from fanfics.services import compute_recommendations
from django.core.cache import cache
from django.contrib.auth import get_user_model

User = get_user_model()

@shared_task
def refresh_recos_for_all_users():
	for user in User.objects.all():
		cache_key = f"recs-user-{user.id}"
		recos = compute_recommendations(user.id)
		fanfics_ids = [r['id'] for r in recos]
		cache.set(cache_key, recos, timeout=3600)
		print(f"Recos updated for user {user.id}")
		reco_obj, _ = Recommendation.objects.update_or_create(user=user)
		reco_obj.fanfictions.set(fanfics_ids)

