import logging
import time

from datetime import timedelta

from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import logout
from django.utils import timezone


class AutoLogout:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.process_request(request)
        if response is not None:
            return response
        return self.get_response(request)

    def process_request(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))

        last_login = request.session.get('last_login')
        now = timezone.now()

        try:
            delay_minutes = int(settings.AUTO_LOGOUT_DELAY)
        except (AttributeError, TypeError, ValueError):
            delay_minutes = None

        if delay_minutes and last_login:
            if now - last_login > timedelta(minutes=delay_minutes):
                logout(request)
                request.session.pop('last_login', None)
                return HttpResponseRedirect(reverse('index'))

        request.session['last_login'] = now

    def process_exception(self, request, exception):
        return HttpResponse(exception)


def metric_middleware(get_response):
    def middleware(request):
        # Get beginning stats
        start_time = time.perf_counter()

        # Process the request
        response = get_response(request)

        # Get ending stats
        end_time = time.perf_counter()

        # Calculate stats
        total_time = end_time - start_time

        # Log the results
        logger = logging.getLogger('debug')
        logger.info(f'Total time: {(total_time):.2f}s')
        print(f'Total time: {(total_time):.2f}s')

        return response

    return middleware
