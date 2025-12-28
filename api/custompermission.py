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
		if request.method in permissions.SAFE_METHODS:
			return True
		return request.user == obj


class IsAuthenticatedOrCreate(permissions.BasePermission):

	def has_permission(self, request, view):
		if request.method == 'POST':
			return True
		return super(IsAuthenticatedOrCreate, self).has_permission(request, view)


class IsTopicStarterOrReadOnly(permissions.BasePermission):
	"""
	Custom permission to only allow the starter of a topic to edit or delete it.
	Read permissions are allowed to any request.
	"""

	def has_object_permission(self, request, view, obj):
		# Read permissions are allowed to any request,
		# so we'll always allow GET, HEAD or OPTIONS requests.
		if request.method in permissions.SAFE_METHODS:
			return True

		# Write permissions are only allowed to the topic starter.
		return obj.starter == request.user


class IsMessageCreatorOrReadOnly(permissions.BasePermission):
	"""
	Custom permission to only allow the creator of a message to edit or delete it.
	Read permissions are allowed to any request.
	"""

	def has_object_permission(self, request, view, obj):
		# Read permissions are allowed to any request,
		# so we'll always allow GET, HEAD or OPTIONS requests.
		if request.method in permissions.SAFE_METHODS:
			return True

		# Write permissions are only allowed to the message creator.
		return obj.created_by == request.user
