from datetime import timedelta
from unittest import mock

from django.core import mail
from django.test import TestCase
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts import services
from apps.accounts.models import FollowStories, FollowUser, Notification, Social
from apps.core.testing import PASSWORD, make_fanfic, make_user

BASE = "/api/v1/accounts/"


class CurrentUserTests(APITestCase):
    def setUp(self):
        self.user = make_user("moi")
        self.client.force_authenticate(self.user)

    def test_anonymous_gets_401(self):
        self.client.force_authenticate(None)
        self.assertEqual(self.client.get(f"{BASE}user/").status_code, 401)

    def test_retrieve_shape_used_by_the_front(self):
        response = self.client.get(f"{BASE}user/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            set(response.data),
            {"user", "profile", "socials", "followed_authors", "followed_fanfics"},
        )
        self.assertEqual(response.data["user"]["username"], "moi")
        self.assertIn("reco_consent_given", response.data["user"]["profile"])

    def test_update_user_and_profile(self):
        response = self.client.patch(
            f"{BASE}user/",
            {
                "user": {"first_name": "Ada"},
                "profile": {"bio": "Autrice", "location": "Paris"},
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Ada")
        self.assertEqual(self.user.accountprofile.location, "Paris")

    def test_update_validation_error(self):
        response = self.client.patch(
            f"{BASE}user/", {"profile": {"location": "x" * 31}}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reco_consent(self):
        response = self.client.put(f"{BASE}consent/", {"reco_consent": "no"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.accountprofile.refresh_from_db()
        self.assertFalse(self.user.accountprofile.reco_consent_given)

    def test_social_networks(self):
        response = self.client.post(
            f"{BASE}social/", {"network": "twitter", "nichandle": "@moi"}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        social = Social.objects.get()
        self.assertEqual(social.user, self.user)

        self.client.force_authenticate(make_user())
        response = self.client.delete(f"{BASE}social/{social.pk}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.force_authenticate(self.user)
        response = self.client.delete(f"{BASE}social/{social.pk}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_disable_account(self):
        response = self.client.delete(f"{BASE}disable/", {"password": "faux"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.delete(f"{BASE}disable/", {"password": PASSWORD})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)
        self.assertEqual(mail.outbox[0].to, [self.user.email])


class FollowTests(APITestCase):
    def setUp(self):
        self.me = make_user()
        self.author = make_user()
        self.fanfic = make_fanfic(self.author)
        self.client.force_authenticate(self.me)

    def test_follow_and_unfollow_author(self):
        url = f"{BASE}follow-author/"
        response = self.client.post(url, {"user_to_id": self.author.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["user_to"]["id"], self.author.id)
        self.assertEqual(
            self.client.post(url, {"user_to_id": self.author.id}).status_code, 400
        )
        self.assertEqual(
            self.client.post(url, {"user_to_id": self.me.id}).status_code, 400
        )
        self.assertEqual(
            self.client.delete(url, {"user_to_id": self.author.id}).status_code, 204
        )
        self.assertFalse(FollowUser.objects.exists())

    def test_follow_story(self):
        url = f"{BASE}follow-story/"
        response = self.client.post(url, {"to_fanfic_id": self.fanfic.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(FollowStories.objects.filter(from_user=self.me).exists())
        self.assertEqual(self.client.post(url, {"to_fanfic_id": 0}).status_code, 400)

    def test_notifications_of_followed_users(self):
        FollowUser.objects.create(user_from=self.me, user_to=self.author)
        services.create_notification(self.author, "a publié", self.fanfic)
        services.create_notification(make_user(), "a publié")
        response = self.client.get(f"{BASE}notifications/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = response.data["results"]
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["target"], self.fanfic.title)
        self.assertNotIn("email", result[0]["user"])


class ContactTests(APITestCase):
    payload = {
        "name": "Jean-Pierre",
        "email": "jp@example.com",
        "message": "Bonjour, une question sur le site.",
        "captcha_token": "token",
    }

    def test_contact_message(self):
        with mock.patch("apps.accounts.services.verify_recaptcha", return_value=True):
            response = self.client.post(f"{BASE}contact-mail/", self.payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(mail.outbox[0].reply_to, ["jp@example.com"])
        self.assertEqual(mail.outbox[0].subject, "Message de contact - Jean-Pierre")

    def test_contact_validation(self):
        with mock.patch("apps.accounts.services.verify_recaptcha", return_value=False):
            response = self.client.post(
                f"{BASE}contact-mail/", {**self.payload, "message": "voir https://spam"}
            )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("captcha_token", response.data)
        self.assertIn("message", response.data)


class ServiceTests(TestCase):
    def test_notifications_are_deduplicated(self):
        user = make_user()
        self.assertTrue(services.create_notification(user, "a liké"))
        self.assertFalse(services.create_notification(user, "a liké"))
        self.assertEqual(Notification.objects.count(), 1)

    def test_recaptcha_handles_network_errors(self):
        with mock.patch(
            "apps.accounts.services.requests.post",
            side_effect=services.requests.ConnectionError,
        ):
            self.assertFalse(services.verify_recaptcha("x"))
        response = mock.Mock(json=lambda: {"success": True, "score": 0.9})
        with mock.patch("apps.accounts.services.requests.post", return_value=response):
            self.assertTrue(services.verify_recaptcha("x"))

    def test_inactive_users_and_reminders(self):
        old = make_user(last_login=timezone.now() - timedelta(days=400))
        recent = make_user(last_login=timezone.now())
        self.assertEqual(services.send_login_reminders(days=14), 1)
        self.assertEqual(mail.outbox[0].to, [old.email])
        self.assertEqual(services.deactivate_inactive_users(days=365), 1)
        old.refresh_from_db()
        recent.refresh_from_db()
        self.assertFalse(old.is_active)
        self.assertTrue(recent.is_active)
