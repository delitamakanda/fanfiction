"""Alias of the ``markdown`` library, kept for ``{% load markdownify %}``."""

from apps.core.templatetags.markdown import register

__all__ = ["register"]
