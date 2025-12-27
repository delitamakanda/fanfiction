import weasyprint
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404
from django.template.loader import render_to_string

from backend import settings
from chapters.models import Chapter
from fanfics.models import Fanfic


def fanfic_pdf(request, fanfic_id):
    """
    Generate pdf output
    """
    try:
        fanfic = Fanfic.objects.get(id=fanfic_id)
        chapters = Chapter.objects.filter(fanfic=fanfic, status="publié")
        html = render_to_string(
            'pdf/fanfic.html', {'fanfic': fanfic, 'chapters': chapters})
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="fanfic_{}.pdf"'.format(
            fanfic.id)
        weasyprint.HTML(string=html).write_pdf(response, stylesheets=[
            weasyprint.CSS(settings.STATIC_ROOT + '/styles/base.css')])
        return response
    except ObjectDoesNotExist:
        raise Http404("Cette fanfiction n'existe pas")
