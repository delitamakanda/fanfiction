from django.test import TestCase
from django.urls import reverse, resolve
from helpcenter.views import communities_view, communities_view_board_topics, communities_view_new_topic, communities_view_topic_messages
from api.models import Board, Topic, Message

class HomeTests(TestCase):
    """
    Tests static pages
    """
    def test_index(self):
        r = self.client.get('/')
        self.assertEqual(r.status_code, 200)


class FaqTests(TestCase):
    """
    Tests for faq
    """
    def test_faq_page(self):
        r = self.client.get('/help/faq')
        self.assertEqual(r.status_code, 200)



class LexiqueTests(TestCase):
    """
    Tests for lexique
    """
    def test_lexique_page(self):
        r = self.client.get('/help/browse/title')
        self.assertEqual(r.status_code, 200)


class ForumTests(TestCase):
    """
    Tests for forums
    """
    def setUp(self):
        self.board = Board.objects.create(name='Anime-Mangas', description='bla bla bla.')
        url = reverse('communities_view')
        self.response = self.client.get(url)

    def test_communities_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_url_resolves_communities_view(self):
        view = resolve('/help/forum')
        self.assertEquals(view.func, communities_view)

    def test_communities_view_contains_link_to_topics_page(self):
        board_topics_url = reverse('board_topics', kwargs={'pk': self.board.pk})
        self.assertContains(self.response, 'href="{0}"'.format(board_topics_url))



class TopicTests(TestCase):
    def setUp(self):
        Board.objects.create(name='Anime-Mangas', description='bla bla bla.')

    def test_topics_view_success_status_code(self):
        url = reverse('board_topics', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_topics_view_not_found_status_code(self):
        url = reverse('board_topics', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_topics_url_resolves_board_topics_view(self):
        view = resolve('/help/forum/1')
        self.assertEquals(view.func, communities_view_board_topics)

    def test_communities_view_contains_link_to_boards(self):
        board_topics_url = reverse('board_topics', kwargs={'pk': 1})
        response = self.client.get(board_topics_url)
        boards_url = reverse('communities_view')
        self.assertContains(response, 'href="{0}"'.format(boards_url))

    def test_board_topics_view_contains_navigation_links(self):
        board_topics_url = reverse('board_topics', kwargs={'pk': 1})
        boards_url = reverse('communities_view')
        new_topic_url = reverse('board_topics_new', kwargs={'pk': 1})

        response = self.client.get(board_topics_url)

        self.assertContains(response, 'href="{0}"'.format(boards_url))
        self.assertContains(response, 'href="{0}"'.format(new_topic_url))


class NewTopicTests(TestCase):
    def setUp(self):
        Board.objects.create(name='Anime-Mangas', description='bla bla bla.')

    def test_new_topic_view_success_status_code(self):
        url = reverse('board_topics_new', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_new_topic_view_not_found_status_code(self):
        url = reverse('board_topics_new', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_new_topic_url_resolves_board_topics_view(self):
        view = resolve('/help/forum/1/new')
        self.assertEquals(view.func, communities_view_new_topic)

    def test_new_topic_view_contains_link_to_boards_topic_view(self):
        new_topics_url = reverse('board_topics_new', kwargs={'pk': 1})
        board_topics_url = reverse('board_topics', kwargs={'pk': 1})
        response = self.client.get(new_topics_url)
        self.assertContains(response, 'href="{0}"'.format(board_topics_url))


class TopicMessagesTests(TestCase):
    def setUp(self):
        Board.objects.create(name='Anime-Mangas', description='bla bla bla.')
        user = User.objects.create_user(username='test', email='doe@example.com', password='test')
        topic = Topic.objects.create(text='lorem ipsum', board=board, starter=user)
        Message.objects.create(text='lorem ipsum sit dolor amet', topic=topic, created_by=user)
        url = reverse('board_topic_message', kwargs={'pk': board.pk, 'topic_pk': topic.pk})
        self.response = self.client.get(url)

        def test_status_code(self):
            self.assertEquals(self.response.status_code, 200)

        def test_view_function(self):
            view = resolve('/forum/1/topics/1')
            self.assertEquals(view.func, board_topic_message)
