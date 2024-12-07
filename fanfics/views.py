from django.shortcuts import render
from fanfics.models import Fanfic

def fanfic_detail(request, id, slug):
	fanfic = Fanfic.objects.get(id=id, slug=slug)
	return render(request, 'fanfic_detail.html', {'fanfic': fanfic})
