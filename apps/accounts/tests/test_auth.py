import re

from django.contrib.auth import get_user_model
from django.core import mail
from django.test import override_settings
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken

from apps.accounts.models import AccountProfile
from apps.core.testing import PASSWORD, make_user

User = get_user_model()
BASE = "/api/v1/accounts/"


class SignupTests(APITestCase):
    def payload(self, **extra):
        return {
            "username": "nouveau",
            "email": "nouveau@example.com",
            "password": PASSWORD,
            "password2": PASSWORD,
            **extra,
        }

    def test_signup_creates_user_and_profile(self):
        response = self.client.post(f"{BASE}signup/", self.payload())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "ok")
        self.assertEqual(response.data["user"]["username"], "nouveau")
        user = User.objects.get(username="nouveau")
        self.assertTrue(AccountProfile.objects.filter(user=user).exists())

    def test_signup_validation(self):
        make_user("pris", email="pris@example.com")
        response = self.client.post(
            f"{BASE}signup/", self.payload(username="PRIS", email="PRIS@example.com")
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)
        self.assertIn("email", response.data)
        response = self.client.post(
            f"{BASE}signup/", self.payload(password2="different")
        )
        self.assertIn("password", response.data)
        response = self.client.post(
            f"{BASE}signup/", self.payload(password="123", password2="123")
        )
        self.assertIn("password", response.data)


class LoginLogoutTests(APITestCase):
    def setUp(self):
        self.user = make_user("lectrice", email="lectrice@example.com")

    def test_login_with_username_or_email(self):
        for login in ("lectrice", "LECTRICE@example.com"):
            response = self.client.post(
                f"{BASE}login/", {"username": login, "password": PASSWORD}
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn("access", response.data)
            self.assertIn("refresh", response.data)
            self.assertEqual(response.data["user"]["username"], "lectrice")
        self.user.refresh_from_db()
        self.assertIsNotNone(self.user.last_login)

    def test_login_errors(self):
        response = self.client.post(f"{BASE}login/", {"username": "lectrice"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(
            f"{BASE}login/", {"username": "lectrice", "password": "wrong"}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.user.is_active = False
        self.user.save()
        response = self.client.post(
            f"{BASE}login/", {"username": "lectrice", "password": PASSWORD}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_jwt_flow_and_logout_all(self):
        tokens = self.client.post(
            f"{BASE}login/", {"username": "lectrice", "password": PASSWORD}
        ).data
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
        response = self.client.get(f"{BASE}user/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        refreshed = self.client.post(
            "/api/auth/token/refresh/", {"refresh": tokens["refresh"]}
        )
        self.assertEqual(refreshed.status_code, status.HTTP_200_OK)

        # What the Vue front sends.
        response = self.client.post(
            f"{BASE}logout/", {"all": "true", "refresh_token": tokens["refresh"]}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(BlacklistedToken.objects.exists())

    def test_logout_requires_authentication(self):
        response = self.client.post(f"{BASE}logout/", {"all": "true"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PasswordTests(APITestCase):
    def setUp(self):
        self.user = make_user("oublieuse", email="oublieuse@example.com")

    @override_settings(FRONTEND_URL="https://front.example")
    def test_reset_flow(self):
        response = self.client.post(
            f"{BASE}password-reset/", {"email": "oublieuse@example.com"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)
        link = re.search(
            r"https://front\.example/password-reset/(\S+)/(\S+)/", mail.outbox[0].body
        )
        self.assertIsNotNone(link)
        uid, token = link.groups()

        url = f"{BASE}password-reset/{uid}/{token}/"
        response = self.client.post(
            url, {"password": "nouveau-mdp-solide", "confirm_password": "x"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(
            url,
            {
                "password": "nouveau-mdp-solide",
                "confirm_password": "nouveau-mdp-solide",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("nouveau-mdp-solide"))

    def test_reset_does_not_reveal_unknown_emails(self):
        response = self.client.post(
            f"{BASE}password-reset/", {"email": "inconnu@example.com"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(mail.outbox, [])

    def test_reset_with_invalid_token(self):
        response = self.client.post(
            f"{BASE}password-reset/MQ/bad-token/",
            {
                "password": "nouveau-mdp-solide",
                "confirm_password": "nouveau-mdp-solide",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_password(self):
        self.client.force_authenticate(self.user)
        url = f"{BASE}change-password/"
        response = self.client.put(
            url, {"old_password": "faux", "new_password": "x-y-z-123456"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("old_password", response.data)
        response = self.client.put(
            url, {"old_password": PASSWORD, "new_password": "x-y-z-123456"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("x-y-z-123456"))
