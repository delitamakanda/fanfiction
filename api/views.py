from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse

class ApiRootView(generics.GenericAPIView):
    name = 'api-root'

    def get(self, request, *args, **kwargs):
        return Response({
            'comments': reverse('comment-list', request=request),
            'category': reverse('category-list', request=request),
            'subcategory': reverse('subcategory-list', request=request),
            'tags': reverse('tag-list', request=request),
            'posts': reverse('post-list', request=request),
            'pages': reverse('all-pages', request=request),
            'genres': reverse('genre-list', request=request),
            'classement': reverse('classement-list', request=request),
            'status': reverse('status-list', request=request),
            'notifications': reverse('notifications', request=request),
            'fanfics': reverse('fanfic-list', request=request)
        })
