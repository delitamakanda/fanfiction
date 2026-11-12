from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q


class EmailAuthBackend(ModelBackend):
    """Authenticate with the username or the e-mail address (case-insensitive)."""

    def authenticate(self, request, username=None, password=None, **kwargs):
        if not username or not password:
            return None
        user_model = get_user_model()
        user = (
            user_model._default_manager.filter(
                Q(username__iexact=username) | Q(email__iexact=username)
            )
            .order_by("pk")
            .first()
        )
        if user is None:
            # Run the hasher anyway to reduce the timing difference.
            user_model().set_password(password)
            return None
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
