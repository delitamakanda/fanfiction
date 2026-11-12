from types import SimpleNamespace
from unittest import mock

from rest_framework import status
from rest_framework.test import APITestCase

from apps.chapters.models import Chapter
from apps.chapters.services import SummaryGenerationError
from apps.core.choices import PublicationStatus
from apps.core.testing import make_chapter, make_fanfic, make_user


class ChapterApiTests(APITestCase):
    def setUp(self):
        self.author = make_user("author")
        self.fanfic = make_fanfic(self.author)
        self.published = make_chapter(self.fanfic, title="Un")
        self.draft = make_chapter(
            self.fanfic, title="Deux", status=PublicationStatus.DRAFT
        )

    def test_list_by_fanfic_hides_drafts_from_readers(self):
        response = self.client.get(f"/api/v1/chapters/{self.fanfic.id}/list/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([c["title"] for c in response.data["results"]], ["Un"])
        self.assertEqual(response.data["results"][0]["status"], "Publié")

        self.client.force_authenticate(self.author)
        response = self.client.get(f"/api/v1/chapters/{self.fanfic.id}/list/")
        self.assertEqual([c["title"] for c in response.data["results"]], ["Un", "Deux"])

    def test_detail(self):
        response = self.client.get(f"/api/v1/chapters/{self.published.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["text"], self.published.text)
        response = self.client.get(f"/api/v1/chapters/{self.draft.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_requires_owning_the_fanfic(self):
        payload = {"fanfic_id": self.fanfic.id, "title": "Trois", "text": "Suite"}
        self.client.force_authenticate(make_user())
        response = self.client.post("/api/v1/chapters/create/", payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("fanfic_id", response.data)

        self.client.force_authenticate(self.author)
        response = self.client.post("/api/v1/chapters/create/", payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        chapter = Chapter.objects.get(pk=response.data["id"])
        self.assertEqual(
            (chapter.author, chapter.order, chapter.status),
            (self.author, 2, "brouillon"),
        )

    def test_create_validation_error(self):
        self.client.force_authenticate(self.author)
        response = self.client.post(
            "/api/v1/chapters/create/",
            {"fanfic_id": self.fanfic.id, "title": " ", "text": "x"},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)

    def test_only_author_can_update(self):
        url = f"/api/v1/chapters/{self.published.id}/"
        self.client.force_authenticate(make_user())
        self.assertEqual(
            self.client.patch(url, {"title": "Hack"}).status_code,
            status.HTTP_403_FORBIDDEN,
        )
        self.client.force_authenticate(self.author)
        response = self.client.patch(url, {"status": "brouillon"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(response.data["published"])

    def test_autosave_creates_then_updates_a_draft(self):
        url = f"/api/v1/chapters/{self.fanfic.id}/autosave"
        self.client.force_authenticate(self.author)
        response = self.client.post(url, {"title": "Brouillon", "text": "Début"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["created"])
        self.assertEqual(response.data["status"], "brouillon")
        chapter_id = response.data["id"]

        response = self.client.post(url, {"id": chapter_id, "text": "Début et suite"})
        self.assertFalse(response.data["created"])
        self.assertEqual(Chapter.objects.get(pk=chapter_id).text, "Début et suite")

    def test_autosave_on_someone_else_fanfic(self):
        self.client.force_authenticate(make_user())
        response = self.client.post(
            f"/api/v1/chapters/{self.fanfic.id}/autosave", {"title": "x", "text": "y"}
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class SummaryApiTests(APITestCase):
    def setUp(self):
        self.client.force_authenticate(make_user())

    def test_styles(self):
        response = self.client.get("/api/v1/chapters/styles")
        self.assertIn("neutre", response.data)

    def test_generate_summary_calls_the_provider(self):
        completion = SimpleNamespace(
            choices=[
                SimpleNamespace(message=SimpleNamespace(content="Il était une fois"))
            ]
        )
        client = mock.Mock()
        client.chat.completions.create.return_value = completion
        with mock.patch("apps.chapters.services._openai_client", return_value=client):
            response = self.client.post(
                "/api/v1/chapters/generate",
                {"prompt": "Un château", "style": "comique"},
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["generated_summary"], "Il était une fois")
        messages = client.chat.completions.create.call_args.kwargs["messages"]
        self.assertIn("comique", messages[0]["content"])

    def test_generate_summary_validation_and_errors(self):
        response = self.client.post(
            "/api/v1/chapters/generate", {"prompt": "x", "style": "gore"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        with mock.patch(
            "apps.chapters.services.generate_summary",
            side_effect=SummaryGenerationError,
        ):
            response = self.client.post("/api/v1/chapters/generate", {"prompt": "x"})
        self.assertEqual(response.status_code, status.HTTP_502_BAD_GATEWAY)

    def test_requires_authentication(self):
        self.client.force_authenticate(None)
        response = self.client.post("/api/v1/chapters/generate", {"prompt": "x"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
