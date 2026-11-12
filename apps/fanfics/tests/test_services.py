from django.core.cache import cache
from django.test import TestCase

from apps.core.testing import make_fanfic, make_user
from apps.fanfics import services, tasks
from apps.fanfics.models import Recommendation, UserFavorite


class RecommendationServiceTests(TestCase):
    def test_readers_who_liked_x_also_liked_y(self):
        me, other = make_user(), make_user()
        shared, suggested = make_fanfic(), make_fanfic()
        UserFavorite.objects.create(user=me, fanfiction=shared)
        UserFavorite.objects.create(user=other, fanfiction=shared)
        UserFavorite.objects.create(user=other, fanfiction=suggested)

        recs = services.compute_recommendations(me.pk)

        self.assertEqual([rec["id"] for rec in recs], [suggested.id])

    def test_tasks_refresh_and_purge(self):
        consenting, opted_out = make_user(), make_user()
        opted_out.accountprofile.reco_consent_given = False
        opted_out.accountprofile.save()
        Recommendation.objects.create(user=opted_out)

        self.assertEqual(tasks.refresh_recos_for_all_users(), 1)
        self.assertTrue(Recommendation.objects.filter(user=consenting).exists())
        self.assertIsNotNone(
            cache.get(services.recommendations_cache_key(consenting.pk))
        )

        self.assertEqual(tasks.purge_recs_from_opted_out_users(), 1)
        self.assertFalse(Recommendation.objects.filter(user=opted_out).exists())
