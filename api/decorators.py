from django.urls import reverse
from django.http import HttpResponseRedirect

def login_check(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func
