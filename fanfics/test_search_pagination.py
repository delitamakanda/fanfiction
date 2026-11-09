from unittest import skipUnless

from django.contrib.auth.models import User
from django.db import connection
from django.test import TestCase
from rest_framework.test import APIClient

from categories.models import Category, SubCategory
from fanfics.models import Fanfic

URL = '/api/v1/fanfics/'


class FanficApiBase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user('alice', password='x')
        cls.other = User.objects.create_user('bob', password='x')
        cls.cat = Category.objects.create(name='Anime')
        cls.cat2 = Category.objects.create(name='Livres')
        cls.sub = SubCategory.objects.create(name='Shonen', category=cls.cat)
        cls.sub2 = SubCategory.objects.create(name='Fantasy', category=cls.cat2)

    def make(self, title, author=None, status='publié', category=None, **kwargs):
        category = category or self.cat
        sub = self.sub if category == self.cat else self.sub2
        return Fanfic.objects.create(
            title=title, slug=title.lower().replace(' ', '-'),
            author=author or self.author, status=status, genres='RO',
            category=category, subcategory=sub, **kwargs)

    def results(self, response):
        return [item['title'] for item in response.data['results']]


class PaginationTests(FanficApiBase):
    def setUp(self):
        for i in range(12):
            self.make(f'Story {i:02d}')

    def test_limit_offset_nominal(self):
        response = APIClient().get(URL, {'limit': 5, 'offset': 5})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 12)
        self.assertEqual(len(response.data['results']), 5)
        self.assertIn('offset=10', response.data['next'])
        self.assertIsNotNone(response.data['previous'])

    def test_default_limit_is_20(self):
        for i in range(12, 25):
            self.make(f'Story {i:02d}')
        response = APIClient().get(URL)
        self.assertEqual(len(response.data['results']), 20)

    def test_invalid_limit_is_400(self):
        for value in ('-1', 'abc', '0'):
            with self.subTest(limit=value):
                response = APIClient().get(URL, {'limit': value})
                self.assertEqual(response.status_code, 400)
        self.assertEqual(APIClient().get(URL, {'offset': '-3'}).status_code, 400)

    def test_limit_is_capped(self):
        for i in range(12, 130):
            self.make(f'Story {i:03d}')
        response = APIClient().get(URL, {'limit': 5000})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 100)

    def test_legacy_page_parameters(self):
        response = APIClient().get(URL, {'page': 2, 'page_size': 5})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 5)
        first = APIClient().get(URL, {'limit': 5, 'offset': 5})
        self.assertEqual(self.results(response), self.results(first))
        self.assertEqual(APIClient().get(URL, {'page': 0}).status_code, 400)


class FilterAndVisibilityTests(FanficApiBase):
    def setUp(self):
        self.make('Dragon Rouge')
        self.make('Livre Bleu', author=self.other, category=self.cat2, completed=True)
        self.make('Brouillon Secret', status='brouillon')

    def test_filters_are_applied(self):
        client = APIClient()
        self.assertEqual(self.results(client.get(URL, {'author': 'bob'})), ['Livre Bleu'])
        self.assertEqual(self.results(client.get(URL, {'category': 'livres'})), ['Livre Bleu'])
        self.assertEqual(self.results(client.get(URL, {'completed': 'true'})), ['Livre Bleu'])
        self.assertEqual(
            self.results(client.get(URL, {'genres': 'RO', 'author': 'alice'})), ['Dragon Rouge'])

    def test_drafts_hidden_from_anonymous_and_others(self):
        self.assertNotIn('Brouillon Secret', self.results(APIClient().get(URL)))
        client = APIClient()
        client.force_authenticate(self.other)
        self.assertNotIn('Brouillon Secret', self.results(client.get(URL)))
        self.assertEqual(client.get(URL + 'brouillon-secret/').status_code, 404)

    def test_author_sees_own_draft(self):
        client = APIClient()
        client.force_authenticate(self.author)
        self.assertIn('Brouillon Secret', self.results(client.get(URL)))


class SearchTests(FanficApiBase):
    def setUp(self):
        self.make('Dragon Rouge', synopsis='Une quête épique')
        self.make('Autre histoire', synopsis='Le dragon rouge dort', description='calme')
        self.make('Brouillon dragon', status='brouillon', synopsis='dragon rouge')

    def test_search_matches(self):
        response = APIClient().get(URL, {'search': 'dragon rouge'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(set(self.results(response)), {'Dragon Rouge', 'Autre histoire'})

    def test_search_by_author(self):
        self.make('Zzz', author=self.other)
        self.assertEqual(self.results(APIClient().get(URL, {'search': 'bob'})), ['Zzz'])

    def test_too_short_is_400(self):
        response = APIClient().get(URL, {'search': 'a'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('au moins', str(response.data['search'][0]))

    def test_empty_search_returns_list(self):
        response = APIClient().get(URL, {'search': ''})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 2)

    def test_search_never_returns_foreign_draft(self):
        anonymous = APIClient().get(URL, {'search': 'dragon'})
        self.assertNotIn('Brouillon dragon', self.results(anonymous))
        client = APIClient()
        client.force_authenticate(self.other)
        self.assertNotIn('Brouillon dragon', self.results(client.get(URL, {'search': 'dragon'})))

    def test_author_search_includes_own_draft(self):
        client = APIClient()
        client.force_authenticate(self.author)
        self.assertIn('Brouillon dragon', self.results(client.get(URL, {'search': 'dragon'})))

    @skipUnless(connection.vendor == 'postgresql', 'PostgreSQL full-text search only')
    def test_ranking_prefers_title_over_synopsis(self):
        titles = self.results(APIClient().get(URL, {'search': 'dragon'}))
        self.assertEqual(titles[0], 'Dragon Rouge')
