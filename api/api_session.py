import json

from django.http import JsonResponse
from django.middleware.csrf import get_token


def get_csrf(request):
    response = JsonResponse({'detail': 'CSRF cookie set'})
    response['X-CSRFToken'] = get_token(request)
    return response
