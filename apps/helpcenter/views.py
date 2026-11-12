"""Server-rendered help pages (lexicon, FAQ), embeddable in an iframe."""

from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from apps.helpcenter.models import FoireAuxQuestions, Lexique

CACHE_TIMEOUT = 60 * 60


@cache_page(CACHE_TIMEOUT)
@xframe_options_exempt
def browse_by_title(request, initial=None):
    words = Lexique.objects.order_by("title")
    if initial:
        words = words.filter(title__istartswith=initial)
    return render(request, "help/dico.html", {"words": words, "initial": initial})


@method_decorator(xframe_options_exempt, name="dispatch")
class SearchSubmitView(View):
    template_name = "help/search_submit.html"
    response_message = "Search"

    def post(self, request):
        query = request.POST.get("search", "").strip()
        context = {
            "title": self.response_message,
            "query": query,
            "items": Lexique.objects.filter(title__icontains=query) if query else [],
            "words": Lexique.objects.order_by("title"),
        }
        return render(request, self.template_name, context)


# Read-only search called by intercooler from the embedded page.
@method_decorator(csrf_exempt, name="dispatch")
class SearchAjaxSubmitView(SearchSubmitView):
    template_name = "help/search_results.html"
    response_message = ""


@cache_page(CACHE_TIMEOUT)
@xframe_options_exempt
def foire_aux_questions_view(request):
    questions = FoireAuxQuestions.objects.order_by("libelle", "order")
    return render(request, "help/faq.html", {"questions": questions})
