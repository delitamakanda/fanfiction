from datetime import datetime, timedelta

from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import logout

class AutoLogout:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_request(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('index'))

        try:
            if datetime.now() - request.session['last_login'] > timedelta(0, settings.AUTO_LOGOUT_DELAY * 60, 0):
                logout(request)
                del request.session['last_login']
                return HttpResponseRedirect(reverse('index'))
        except KeyError:
            pass

        request.session['last_login'] = datetime.now()

    def process_exception(self, request, exception):
        return HttpResponse(exception)
