"""``{% load gravatar %}``: ``{{ user|gravatar }}`` returns the avatar URL."""

import hashlib
from urllib.parse import urlencode

from django import template

register = template.Library()


@register.filter
def gravatar(user, size: int = 100) -> str:
    email = (getattr(user, "email", "") or "").strip().lower().encode("utf-8")
    digest = hashlib.md5(email, usedforsecurity=False).hexdigest()
    return f"https://www.gravatar.com/avatar/{digest}?{urlencode({'d': 'retro', 's': size})}"
