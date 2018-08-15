from django.shortcuts import render
from help.models import Lexique

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
