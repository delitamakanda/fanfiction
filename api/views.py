from rest_framework import generics, permissions
from rest_framework.response import Response

class ApiRootView(generics.GenericAPIView):
	name = 'api-root'
	permission_classes = [permissions.AllowAny,]

	def get(self, request, *args, **kwargs):
		return Response({
			'comments': 'http://localhost:8000/api/comments/',
			'categories': 'http://localhost:8000/api/categories/',
			'subcategory': 'http://localhost:8000/api/categories/subcategory/',
			'tags': 'http://localhost:8000/api/posts/tags/',
			'posts': 'http://localhost:8000/api/posts/',
			'pages': 'http://localhost:8000/api/pages/',
			'genres': 'http://localhost:8000/api/fanfics/genres/',
			'classement': 'http://localhost:8000/api/fanfics/classement/',
			'status': 'http://localhost:8000/api/fanfics/status/',
			'notifications': 'http://localhost:8000/api/notifications/',
			'fanfics': 'http://localhost:8000/api/fanfics/',
		})
