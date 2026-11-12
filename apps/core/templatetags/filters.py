"""``{% load filters %}``: ``{{ form.field|addclass:"css classes" }}``."""

import re

from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()

_CLASS_ATTR = re.compile(r'class=(["\'])(.*?)\1')
_FIRST_TAG = re.compile(r"^(\s*<[a-zA-Z][\w-]*)")


@register.filter(name="addclass")
def addclass(value, css_class: str):
    """Add CSS classes to a form field, or to the first tag of rendered HTML."""
    if hasattr(value, "as_widget"):
        existing = value.field.widget.attrs.get("class", "")
        return value.as_widget(attrs={"class": f"{existing} {css_class}".strip()})

    html = str(value)
    if not html:
        return value
    css = escape(css_class)
    match = _CLASS_ATTR.search(html)
    if match:
        if css_class in match.group(2).split():
            return value
        quote, classes = match.group(1), match.group(2)
        replacement = f"class={quote}{classes} {css}{quote}"
        return mark_safe(html[: match.start()] + replacement + html[match.end() :])  # noqa: S308
    return mark_safe(_FIRST_TAG.sub(rf'\1 class="{css}"', html, count=1))  # noqa: S308
