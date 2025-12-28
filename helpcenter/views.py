from django.conf import settings
from django.core import cache
from django.shortcuts import render
from django.utils.decorators import method_decorator

from django.views.generic import View
from django.template import loader
from django.http import HttpResponse
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page
from django.core.cache.backends.base import DEFAULT_TIMEOUT

from helpcenter.models import Lexique, FoireAuxQuestions

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

@cache_page(60 * 60 * 24)
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


@cache_page(60 * 60 * 20)
@xframe_options_exempt
def foire_aux_questions_view(request):
    cache_key = 'foire_aux_questions_view'
    questions = cache.get(cache_key)

    if questions is None:
        questions = FoireAuxQuestions.objects.all()
        cache.set(cache_key, questions, 60 * 60 * 24)
    return render(request, 'help/faq.html', {'questions': questions})

