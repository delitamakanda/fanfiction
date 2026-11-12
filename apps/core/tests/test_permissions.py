from types import SimpleNamespace

from django.contrib.auth.models import AnonymousUser
from django.test import SimpleTestCase

from apps.core.permissions import IsAdminOrReadOnly, IsOwner, IsOwnerOrReadOnly


def request(method, user):
    return SimpleNamespace(method=method, user=user)


class PermissionTests(SimpleTestCase):
    def setUp(self):
        self.owner = SimpleNamespace(pk=1, is_staff=False, is_authenticated=True)
        self.other = SimpleNamespace(pk=2, is_staff=False, is_authenticated=True)
        self.staff = SimpleNamespace(pk=3, is_staff=True, is_authenticated=True)

    def test_admin_or_read_only(self):
        permission = IsAdminOrReadOnly()
        self.assertTrue(
            permission.has_permission(request("GET", AnonymousUser()), None)
        )
        self.assertFalse(permission.has_permission(request("POST", self.owner), None))
        self.assertTrue(permission.has_permission(request("POST", self.staff), None))

    def test_owner_or_read_only_uses_view_owner_field(self):
        permission = IsOwnerOrReadOnly()
        view = SimpleNamespace(owner_field="starter")
        obj = SimpleNamespace(starter_id=1)
        self.assertTrue(
            permission.has_object_permission(request("GET", self.other), view, obj)
        )
        self.assertTrue(
            permission.has_object_permission(request("PUT", self.owner), view, obj)
        )
        self.assertFalse(
            permission.has_object_permission(request("PUT", self.other), view, obj)
        )

    def test_owner_defaults_to_user_field(self):
        permission = IsOwner()
        obj = SimpleNamespace(user_id=1)
        self.assertTrue(
            permission.has_object_permission(request("GET", self.owner), None, obj)
        )
        self.assertFalse(
            permission.has_object_permission(request("GET", self.other), None, obj)
        )
