"""Markdown rendering for user-generated content."""

import markdown
from django.utils.safestring import SafeString, mark_safe


def render_user_markdown(text: str) -> SafeString:
    """Render Markdown written by users: raw HTML is escaped, not rendered."""
    md = markdown.Markdown(extensions=["extra"])
    md.preprocessors.deregister("html_block")
    md.inlinePatterns.deregister("html")
    return mark_safe(md.convert(text or ""))  # noqa: S308 - raw HTML is disabled
