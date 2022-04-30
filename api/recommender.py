import redis
import os

from django.conf import settings
from fanfics.models import Fanfic

# connect to redis

# url = settings.REDIS_URL
url = os.getenv('REDIS_URL', 'redis://localhost:6379')
r = redis.StrictRedis.from_url(url)

class Recommender(object):

    def get_fanfic_key(self, id):
        return 'fanfic:{}:liked_with'.format(id)

    def fanfics_liked(self, fanfics):
        fanfics_ids = [p.id for p in fanfics]

        for fanfic_id in fanfics_ids:
            for with_id in fanfics_ids:
                # get the others fanfics liked in each fanfic
                if fanfic_id != with_id:
                    # increment score for fanfic liked
                    r.zincrby(
                        name=self.get_fanfic_key(fanfic_id),
                        value=with_id,
                        amount=1
                    )


    def suggest_fanfics_for(self, fanfics, max_results=6):
        fanfic_ids = [p.id for p in fanfics]
        if len(fanfics) == 1:
            # only 1 item
            suggestions = r.zrange(
                self.get_fanfic_key(fanfic_ids[0]),
                0, -1, desc=True)[:max_results]
        else:
            # generate a temp key
            flat_ids = ''.join([str(id) for id in fanfic_ids])
            tmp_key = 'tmp_{}'.format(flat_ids)
            # multiple fanfics, combine scores of all fanfics
            # store the resulting stored set in a temp key
            keys = [self.get_fanfic_key(id) for id in fanfic_ids]
            r.zunionstore(tmp_key, keys)
            # remove ids for the fanfics the recommandation is for
            r.zrem(tmp_key, *fanfic_ids)
            # get the fanfic ids by their score desc sort
            suggestions = r.zrange(tmp_key, 0, -1, desc=True)[:max_results]
            # remove the temp key
            r.delete(tmp_key)
        suggested_fanfics_ids = [int(id) for id in suggestions]

        # get the suggested fanfics and sort by order of appearance
        suggested_fanfics = list(Fanfic.objects.filter(id__in=suggested_fanfics_ids))
        suggested_fanfics.sort(key=lambda x: suggested_fanfics_ids.index(x.id))

        return suggested_fanfics


    def clear_fanfics(self):
        for id in Fanfic.objects.values_list('id', flat=True):
            r.delete(self.get_fanfic_key(id))
