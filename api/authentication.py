from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

class EmailAuthBackend(ModelBackend):

    """
    Authenticate using e-mail or username
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if not username or not password:
            return None
        user_model = get_user_model()
        try:
            user = user_model.objects.get(Q(username__iexact=username) | Q(email__iexact=username))
        except user_model.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user

        return None
