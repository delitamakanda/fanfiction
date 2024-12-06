import weasyprint

from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.views.generic import View, UpdateView, ListView
from django.utils import timezone
from django.template import loader
from django.template.loader import get_template, render_to_string
from django.http import HttpResponse, Http404
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.core.cache.backends.base import DEFAULT_TIMEOUT

from helpcenter.models import Lexique, FoireAuxQuestions

from fanfics.models import Fanfic
from chapters.models import Chapter

from accounts.models import AccountProfile

from api.decorators import login_check

from markdownx.utils import markdownify

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

@cache_page(60 * 15)
@xframe_options_exempt
def browse_by_title(request, initial=None):
    if initial:
        words = Lexique.objects.filter(
            title__istartswith=initial).order_by('title')
    else:
        words = Lexique.objects.all().order_by('title')

    return render(request, 'help/dico.html', {
        'words': words,
        'initial': initial,
    })


@method_decorator(xframe_options_exempt, name='dispatch')
@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class SearchSubmitView(View):
    template = 'help/search_submit.html'
    response_message = 'Search'

    def post(self, request):
        template = loader.get_template(self.template)
        query = request.POST.get('search', '')
        words = Lexique.objects.all().order_by('title')
        items = Lexique.objects.filter(title__icontains=query)
        context = {'title': self.response_message,
                   'query': query, 'items': items, 'words': words}
        rendered_template = template.render(context, request)
        return HttpResponse(rendered_template, content_type='text/html')


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(xframe_options_exempt, name='dispatch')
@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class SearchAjaxSubmitView(SearchSubmitView):
    template = 'help/search_results.html'
    response_message = ''


questions = FoireAuxQuestions.objects.all().order_by('libelle')


@xframe_options_exempt
def foire_aux_questions_view(request):
    for question in questions:
        question.reponse = markdownify(question.reponse)
    return render(request, 'help/faq.html', {'questions': questions})

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
