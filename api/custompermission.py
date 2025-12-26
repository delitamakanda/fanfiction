from rest_framework import permissions

class IsCurrentAuthorOrReadOnly(permissions.BasePermission):

	def has_object_permission(self, request, view, obj):
		if request.method in permissions.SAFE_METHODS:
			return True
		else:
			return obj.author == request.user


class IsCurrentSessionOrReadOnly(permissions.BasePermission):
	"""
	Handles permissions for the current session. The basic rules are

	 - authenticated users may PUT
	 - nobody else can accessed
	"""
	def has_permission(self, request, view):
		if request.method in ['PUT'] and request.session.get('comment_session_id'):
			return True
		return None


class IsCurrentUserOrReadonly(permissions.BasePermission):
	"""
	Handles permissions for users.  The basic rules are

	 - owner may GET, PUT, POST, DELETE
	 - nobody else can access
	 """

	def has_object_permission(self, request, view, obj):
		return request.user == obj.user


class IsUserOrReadonly(permissions.BasePermission):
	"""
	Handles permissions for users.  The basic rules are

	 - owner may GET, PUT, POST, DELETE
	 - nobody else can access
	 """

	def has_object_permission(self, request, view, obj):
		return request.user == obj


class IsAuthenticatedOrCreate(permissions.BasePermission):

	def has_permission(self, request, view):
		if request.method == 'POST':
			return True
		return request.user and request.user.is_authenticated
