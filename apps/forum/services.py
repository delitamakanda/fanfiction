from django.db import transaction
from django.db.models import F
from django.utils import timezone

from apps.forum.models import Message, Topic


@transaction.atomic
def start_topic(*, board, starter, subject: str, text: str) -> Topic:
    """Create a topic with its first message."""
    topic = Topic.objects.create(board=board, starter=starter, subject=subject)
    Message.objects.create(topic=topic, created_by=starter, text=text)
    return topic


@transaction.atomic
def reply(*, topic: Topic, author, text: str) -> Message:
    message = Message.objects.create(topic=topic, created_by=author, text=text)
    Topic.objects.filter(pk=topic.pk).update(last_updated=timezone.now())
    return message


def edit_message(message: Message, *, editor, text: str) -> Message:
    message.text = text
    message.updated_by = editor
    message.updated_at = timezone.now()
    message.save(update_fields=["text", "updated_by", "updated_at"])
    return message


def register_topic_view(topic: Topic, session) -> None:
    session_key = f"viewed_topic_{topic.pk}"
    if not session.get(session_key):
        Topic.objects.filter(pk=topic.pk).update(views=F("views") + 1)
        session[session_key] = True
