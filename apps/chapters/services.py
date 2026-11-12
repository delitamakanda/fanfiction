"""Business logic of the chapters app."""

import logging
from functools import lru_cache

from django.conf import settings
from django.db import transaction

from apps.chapters.models import Chapter
from apps.core.choices import PublicationStatus

logger = logging.getLogger(__name__)

SUMMARY_STYLES = ["neutre", "romantique", "dramatique", "comique", "mystérieux"]


class SummaryGenerationError(Exception):
    """The text generation provider failed."""


@lru_cache(maxsize=1)
def _openai_client():
    from openai import OpenAI  # imported lazily: optional at import time

    return OpenAI(api_key=settings.OPENAI_API_KEY)


def generate_summary(prompt: str, style: str = "neutre") -> str:
    """Ask the LLM for a short immersive text in the requested ``style``."""
    system_message = (
        "Tu es un auteur expert de fanfiction.\n"
        f"Style demandé : {style}.\n"
        "Ecris un texte immersif, mature et cohérent."
    )
    try:
        response = _openai_client().chat.completions.create(
            model=settings.OPENAI_MODEL,
            temperature=0.9,
            max_tokens=600,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt},
            ],
        )
    except Exception as exc:
        logger.exception("Summary generation failed")
        raise SummaryGenerationError(str(exc)) from exc
    return response.choices[0].message.content or ""


@transaction.atomic
def autosave(
    *, fanfic, author, data: dict, chapter_id: int | None = None
) -> tuple[Chapter, bool]:
    """Save a draft of a chapter while the author is typing.

    Updates ``chapter_id`` when given (it must belong to ``author``), otherwise
    creates a new draft. Returns ``(chapter, created)``.
    """
    fields = {
        key: data[key]
        for key in ("title", "description", "text", "order")
        if key in data
    }
    if chapter_id is not None:
        chapter = Chapter.objects.select_for_update().get(
            pk=chapter_id, fanfic=fanfic, author=author
        )
        for key, value in fields.items():
            setattr(chapter, key, value)
        chapter.save()
        return chapter, False
    chapter = Chapter.objects.create(
        fanfic=fanfic, author=author, status=PublicationStatus.DRAFT, **fields
    )
    return chapter, True
