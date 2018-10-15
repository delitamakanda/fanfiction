import weasyprint

from django.conf import settings
from django.shortcuts import render

from django.views.generic import View
from django.template import loader
from django.template.loader import get_template, render_to_string
from django.http import HttpResponse, Http404
from django.core.exceptions import ObjectDoesNotExist

from api.models import Lexique
from api.models import FoireAuxQuestions
from api.models import Fanfic
from api.models import Chapter
from api.models import Board
from api.models import Topic
from api.models import Message

from markdownx.utils import markdownify

# Create your views here.
def browse_by_title(request, initial=None):
    if initial:
        words = Lexique.objects.filter(title__istartswith=initial).order_by('title')
    else:
        words = Lexique.objects.all().order_by('title')

    return render(request, 'help/dico.html', {
        'words': words,
        'initial': initial,
    })


class SearchSubmitView(View):
    template = 'help/search_submit.html'
    response_message = 'Search'

    def post(self, request):
        template = loader.get_template(self.template)
        query = request.POST.get('search', '')
        words = Lexique.objects.all().order_by('title')
        items = Lexique.objects.filter(title__icontains=query)
        context = {'title': self.response_message, 'query': query, 'items': items, 'words': words}
        rendered_template = template.render(context, request)
        return HttpResponse(rendered_template, content_type='text/html')


class SearchAjaxSubmitView(SearchSubmitView):
    template = 'help/search_results.html'
    response_message = ''


questions = FoireAuxQuestions.objects.all().order_by('libelle')
def foire_aux_questions_view(request):
    for question in questions:
        question.reponse = markdownify(question.reponse)
    return render(request, 'help/faq.html', {'questions': questions})


def communities_view(request):
    """
    Communities
    """
    boards = Board.objects.all()

    context = {'boards': boards}
    return render(request, 'help/communities.html', context)


def fanfic_pdf(request, fanfic_id):
    """
    Generate pdf output
    """
    try:
        fanfic = Fanfic.objects.filter(status="publié").get(id=fanfic_id)
        chapters = Chapter.objects.filter(fanfic=fanfic, status="publié")
        html = render_to_string('pdf/fanfic.html', {'fanfic': fanfic, 'chapters': chapters})
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="fanfic_{}.pdf"'.format(fanfic.id)
        weasyprint.HTML(string=html).write_pdf(response, stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + '/styles/base.css')])
        return response
    except ObjectDoesNotExist:
        raise Http404("Cette fanfiction n'existe pas")
