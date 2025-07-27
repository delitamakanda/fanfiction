from django.db.models.aggregates import Count

from fanfics.models import Fanfic, UserFavorite


def compute_recommendations(user_id):
	user_favorites = set(UserFavorite.objects.filter(user_id=user_id).values_list('fanfiction_id', flat=True))
	similar_users = UserFavorite.objects.filter(fanfiction_id__in=user_favorites).exclude(user_id=user_id).values_list('user_id', flat=True)
	recos = (UserFavorite.objects.filter(user_id__in=similar_users).exclude(fanfiction_id__in=user_favorites).values('fanfiction_id').annotate(score=Count('fanfiction_id')).order_by('-score')[:5])
	fanfictions_ids = [r['fanfiction_id'] for r in recos]
	return list(Fanfic.objects.filter(id__in=fanfictions_ids).values('id', 'title', 'synopsis'))
