"""Markdown rendering filters: ``{% load markdown %}``."""

from django import template
from markdownx.utils import markdownify

register = template.Library()


@register.filter(name="markdown")
def markdown(value: str) -> str:
    return markdownify(value or "")


@register.filter(name="show_markdown")
def show_markdown(value: str) -> str:
    return markdownify(value or "")
