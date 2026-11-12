from unittest import mock

from django.core import mail
from django.test import override_settings
from rest_framework import status
from rest_framework.test import APITestCase

from apps.core.choices import PublicationStatus
from apps.core.testing import make_fanfic, make_subcategory, make_user
from apps.fanfics.models import Fanfic, Recommendation

LIST_URL = "/api/v1/fanfics/"


class FanficReadTests(APITestCase):
    def setUp(self):
        self.author = make_user("author")
        self.published = make_fanfic(self.author, title="Publiée")
        self.draft = make_fanfic(
            self.author, status=PublicationStatus.DRAFT, title="Brouillon"
        )

    def test_anonymous_list_hides_drafts(self):
        response = self.client.get(LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            [f["id"] for f in response.data["results"]], [self.published.id]
        )

    def test_author_sees_own_drafts(self):
        self.client.force_authenticate(self.author)
        response = self.client.get(LIST_URL)
        self.assertEqual(response.data["count"], 2)

    def test_draft_detail_is_hidden_from_other_users(self):
        self.client.force_authenticate(make_user())
        response = self.client.get(f"{LIST_URL}{self.draft.slug}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_detail_counts_one_view_per_session(self):
        url = f"{LIST_URL}{self.published.slug}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["views"], 1)
        self.assertIn("users_like", response.data)
        self.client.get(url)
        self.published.refresh_from_db()
        self.assertEqual(self.published.views, 1)

    def test_front_search_on_status_still_works(self):
        response = self.client.get(LIST_URL, {"q": "publié", "ordering": "-created"})
        self.assertEqual(response.data["count"], 1)

    def test_filters_are_applied(self):
        other = make_fanfic(title="Autre", completed=True)
        response = self.client.get(LIST_URL, {"completed": "true"})
        self.assertEqual([f["id"] for f in response.data["results"]], [other.id])
        response = self.client.get(LIST_URL, {"author": "AUTHOR"})
        self.assertEqual(
            [f["id"] for f in response.data["results"]], [self.published.id]
        )

    def test_choices_endpoints(self):
        response = self.client.get(f"{LIST_URL}genres/")
        self.assertEqual(response.data["genres"][0], {"id": "RO", "libelle": "Romance"})
        response = self.client.get(f"{LIST_URL}status/")
        self.assertEqual(
            response.data["status"][1], {"id": "publié", "libelle": "Publié"}
        )


class FanficWriteTests(APITestCase):
    def setUp(self):
        self.author = make_user("writer")
        self.subcategory = make_subcategory()

    def payload(self, **extra):
        return {
            "title": "Ma fanfic",
            "genres": ["RO", "DR"],
            "classement": "g",
            "category": self.subcategory.category_id,
            "subcategory": self.subcategory.id,
            **extra,
        }

    def test_anonymous_cannot_create(self):
        response = self.client.post(LIST_URL, self.payload(), format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_sets_author_and_unique_slug(self):
        self.client.force_authenticate(self.author)
        first = self.client.post(LIST_URL, self.payload(), format="json")
        second = self.client.post(LIST_URL, self.payload(), format="json")
        self.assertEqual(first.status_code, status.HTTP_201_CREATED)
        self.assertEqual(first.data["slug"], "ma-fanfic")
        self.assertEqual(second.data["slug"], "ma-fanfic-2")
        self.assertEqual(Fanfic.objects.filter(author=self.author).count(), 2)
        self.assertEqual(Fanfic.objects.get(slug="ma-fanfic").status, "brouillon")

    def test_subcategory_must_belong_to_category(self):
        self.client.force_authenticate(self.author)
        other = make_subcategory()
        response = self.client.post(
            LIST_URL, self.payload(subcategory=other.id), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("subcategory", response.data)

    def test_only_author_can_update(self):
        fanfic = make_fanfic(self.author)
        url = f"{LIST_URL}{fanfic.slug}/"
        self.client.force_authenticate(make_user())
        response = self.client.patch(url, {"title": "Volée"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(self.author)
        response = self.client.patch(url, {"status": "brouillon"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        fanfic.refresh_from_db()
        self.assertEqual(fanfic.status, "brouillon")


class LikeTests(APITestCase):
    def test_like_and_unlike_keep_total_in_sync(self):
        fanfic = make_fanfic()
        reader = make_user()
        self.client.force_authenticate(reader)
        url = "/api/v1/accounts/like/"
        response = self.client.post(
            url, {"id": fanfic.id, "action": "like"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["is_liked"])
        self.assertEqual(response.data["fanfic"]["total_likes"], 1)
        self.client.post(url, {"id": fanfic.id, "action": "like"}, format="json")
        response = self.client.post(
            url, {"id": fanfic.id, "action": "unlike"}, format="json"
        )
        self.assertEqual(response.data["fanfic"]["total_likes"], 0)

    def test_invalid_action(self):
        self.client.force_authenticate(make_user())
        response = self.client.post(
            "/api/v1/accounts/like/", {"id": make_fanfic().id, "action": "love"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class EmailEndpointsTests(APITestCase):
    def test_share_by_email(self):
        fanfic = make_fanfic()
        response = self.client.post(
            f"{LIST_URL}share/",
            {
                "id": fanfic.id,
                "name": "Ana",
                "email": "ana@example.com",
                "to_email": "bob@example.com",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(mail.outbox[0].to, ["bob@example.com"])
        self.assertIn(f"/fanfics/{fanfic.slug}", mail.outbox[0].body)

    def test_share_rejects_drafts(self):
        draft = make_fanfic(status=PublicationStatus.DRAFT)
        response = self.client.post(
            f"{LIST_URL}share/",
            {
                "id": draft.id,
                "name": "Ana",
                "email": "ana@example.com",
                "to_email": "bob@example.com",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(mail.outbox, [])

    @override_settings(SERVER_EMAIL="moderation@example.com")
    def test_feedback_reports_to_moderators(self):
        response = self.client.post(f"{LIST_URL}feedback/", {"id": make_fanfic().id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(mail.outbox[0].to, ["moderation@example.com"])


class RecommendationTests(APITestCase):
    def setUp(self):
        self.user = make_user()
        self.url = f"{LIST_URL}recommendations/"

    def test_requires_consent(self):
        self.user.accountprofile.reco_consent_given = False
        self.user.accountprofile.save()
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lists_and_clears_recommendations(self):
        fanfic = make_fanfic()
        Recommendation.objects.create(user=self.user).fanfictions.add(fanfic)
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([f["id"] for f in response.data["results"]], [fanfic.id])
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Recommendation.objects.filter(user=self.user).exists())


class PdfExportTests(APITestCase):
    def test_draft_is_not_exported(self):
        draft = make_fanfic(status=PublicationStatus.DRAFT)
        response = self.client.get(f"{LIST_URL}{draft.id}/pdf")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_published_fanfic_is_rendered(self):
        fanfic = make_fanfic()
        with mock.patch("weasyprint.HTML") as html:
            response = self.client.get(f"{LIST_URL}{fanfic.id}/pdf")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response["Content-Type"], "application/pdf")
        self.assertIn(fanfic.title, html.call_args.kwargs["string"])
