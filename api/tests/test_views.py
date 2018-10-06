from django.test import TestCase

class FanfictionPagesTest(TestCase):
    """
    Tests static pages
    """
    def test_index(self):
        r = self.client.get('/')
        self.assertEqual(r.status_code, 200)

    def test_faq_page(self):
        r = self.client.get('/help/faq')
        self.assertEqual(r.status_code, 200)

    def test_lexique_page(self):
        r = self.client.get('/help/browse/title')
        self.assertEqual(r.status_code, 200)
