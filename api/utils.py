import datetime
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from accounts.models import Notification


def create_notification(user, verb, target=None):
    now = timezone.now()
    last_minute = now - datetime.timedelta(seconds=60)
    similar_notifications = Notification.objects.filter(user_id=user.id, verb=verb, created__gte=last_minute)

    if target:
        target_ct = ContentType.objects.get_for_model(target)
        similar_notifications = similar_notifications.filter(target_ct=target_ct, target_id=target.id)

    if not similar_notifications:
        notification = Notification(user=user, verb=verb, target=target)
        notification.save()
        return True
    return False
