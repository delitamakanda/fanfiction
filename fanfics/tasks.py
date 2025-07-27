from celery import shared_task
from fanfics.models import Recommendation
from fanfics.services import compute_recommendations

@shared_task
def recompute_user_recommendations(user_id):
	recs = compute_recommendations(user_id)
	Recommendation.objects.update_or_create(user_id=user_id, defaults={'data':recs})
