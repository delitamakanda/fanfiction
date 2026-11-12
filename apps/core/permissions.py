"""Reusable DRF permissions.

Object permissions only run on detail routes: combine them with a
``has_permission`` class such as ``IsAuthenticatedOrReadOnly``.
"""

from rest_framework import permissions

SAFE_METHODS = permissions.SAFE_METHODS


class IsAdminOrReadOnly(permissions.BasePermission):
    """Anyone can read, only staff users can write."""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Anyone can read, only the owner can write.

    The owner is read from ``view.owner_field`` (default: ``author``).
    """

    owner_field = "author"

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        field = getattr(view, "owner_field", self.owner_field)
        return getattr(obj, f"{field}_id", None) == request.user.pk


class IsOwner(permissions.BasePermission):
    """Only the owner can read or write (``view.owner_field``, default ``user``)."""

    owner_field = "user"

    def has_object_permission(self, request, view, obj):
        field = getattr(view, "owner_field", self.owner_field)
        return getattr(obj, f"{field}_id", None) == request.user.pk
