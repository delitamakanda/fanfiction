from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

from apps.fanfics.models import Fanfic


def fanfic_pdf(request, fanfic_id: int) -> HttpResponse:
    """PDF export of a published fanfic and its published chapters."""
    import weasyprint  # heavy import, only needed here

    fanfic = get_object_or_404(Fanfic.published, pk=fanfic_id)
    chapters = fanfic.chapters.published().order_by("order")
    html = render_to_string("pdf/fanfic.html", {"fanfic": fanfic, "chapters": chapters})
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="fanfic_{fanfic.pk}.pdf"'
    weasyprint.HTML(string=html, base_url=request.build_absolute_uri("/")).write_pdf(
        response
    )
    return response
