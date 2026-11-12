from django.test import TestCase

from apps.core.testing import PASSWORD, make_user
from apps.forum.models import Board, Message, Topic


class ForumPagesTests(TestCase):
    def setUp(self):
        self.user = make_user()
        self.board = Board.objects.create(name="Mangas", description="Discussions")

    def test_board_and_topic_pages(self):
        topic = Topic.objects.create(
            board=self.board, subject="Sujet", starter=self.user
        )
        Message.objects.create(
            topic=topic, created_by=self.user, text="**Salut** <b>x</b>"
        )
        self.assertContains(self.client.get("/api/forum/"), "Mangas")
        self.assertContains(self.client.get(f"/api/forum/{self.board.pk}"), "Sujet")
        response = self.client.get(f"/api/forum/{self.board.pk}/topics/{topic.pk}")
        self.assertContains(response, "<strong>Salut</strong>", html=True)
        self.assertNotContains(response, "<b>x</b>")
        topic.refresh_from_db()
        self.assertEqual(topic.views, 1)

    def test_new_topic_requires_login(self):
        url = f"/api/forum/{self.board.pk}/new"
        response = self.client.post(url, {"subject": "Hop", "text": "Contenu"})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Topic.objects.exists())

        self.client.login(username=self.user.username, password=PASSWORD)
        response = self.client.post(url, {"subject": "Hop", "text": "Contenu"})
        topic = Topic.objects.get()
        self.assertRedirects(response, f"/api/forum/{self.board.pk}/topics/{topic.pk}")
        self.assertEqual(topic.messages.get().created_by, self.user)

    def test_only_author_can_edit_message(self):
        topic = Topic.objects.create(
            board=self.board, subject="Sujet", starter=self.user
        )
        message = Message.objects.create(
            topic=topic, created_by=self.user, text="Avant"
        )
        url = f"/api/forum/{self.board.pk}/topics/{topic.pk}/message/{message.pk}/edit"
        other = make_user()
        self.client.login(username=other.username, password=PASSWORD)
        self.assertEqual(self.client.post(url, {"text": "Piraté"}).status_code, 404)
        self.client.login(username=self.user.username, password=PASSWORD)
        self.client.post(url, {"text": "Après"})
        message.refresh_from_db()
        self.assertEqual((message.text, message.updated_by), ("Après", self.user))
