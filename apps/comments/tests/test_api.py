from rest_framework import status
from rest_framework.test import APITestCase

from apps.comments.models import Comment
from apps.core.choices import PublicationStatus
from apps.core.testing import make_chapter, make_fanfic, make_user

URL = "/api/v1/comments/"


class CommentApiTests(APITestCase):
    def setUp(self):
        self.fanfic = make_fanfic()
        self.chapter = make_chapter(self.fanfic)
        self.reader = make_user()

    def test_anyone_can_read_comments_of_a_fanfic(self):
        Comment.objects.create(
            author=self.reader, fanfic=self.fanfic, body="Très bien écrit"
        )
        response = self.client.get(URL, {"fanfic": self.fanfic.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"][0]["fanfic_title"], self.fanfic.title)
        self.assertFalse(response.data["results"][0]["is_author"])

    def test_create_comment_and_reply(self):
        self.client.force_authenticate(self.reader)
        response = self.client.post(
            URL,
            {
                "fanfic": self.fanfic.id,
                "chapter": self.chapter.id,
                "body": "  J'adore !  ",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["body"], "J'adore !")
        self.assertTrue(response.data["is_author"])

        reply = self.client.post(
            URL,
            {
                "fanfic": self.fanfic.id,
                "in_reply_to_id": response.data["id"],
                "body": "Moi aussi",
            },
        )
        self.assertEqual(reply.status_code, status.HTTP_201_CREATED)
        self.assertEqual(reply.data["in_reply_to"]["id"], response.data["id"])

    def test_validation(self):
        self.client.force_authenticate(self.reader)
        other_chapter = make_chapter(make_fanfic())
        response = self.client.post(
            URL,
            {
                "fanfic": self.fanfic.id,
                "chapter": other_chapter.id,
                "body": "Hors sujet",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(URL, {"fanfic": self.fanfic.id, "body": "abc"})
        self.assertIn("body", response.data)
        draft = make_fanfic(status=PublicationStatus.DRAFT)
        response = self.client.post(URL, {"fanfic": draft.id, "body": "Brouillon !"})
        self.assertIn("fanfic", response.data)

    def test_only_author_can_edit_or_delete(self):
        comment = Comment.objects.create(
            author=self.reader, fanfic=self.fanfic, body="Premier"
        )
        self.client.post(URL, {"fanfic": self.fanfic.id, "body": "Anonyme"})
        self.assertEqual(Comment.objects.count(), 1)

        self.client.force_authenticate(make_user())
        response = self.client.delete(f"{URL}{comment.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(self.reader)
        response = self.client.patch(f"{URL}{comment.id}/", {"body": "Premier, édité"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(f"{URL}{comment.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
