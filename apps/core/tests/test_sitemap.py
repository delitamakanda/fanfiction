from django.test import TestCase

from apps.core.choices import PublicationStatus
from apps.core.testing import make_fanfic


class SitemapTests(TestCase):
    def test_sitemap_lists_published_fanfics_only(self):
        published = make_fanfic(title="Visible")
        draft = make_fanfic(title="Cachée", status=PublicationStatus.DRAFT)
        response = self.client.get("/sitemap.xml")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f"/fanfics/{published.slug}/")
        self.assertNotContains(response, draft.slug)
        self.assertContains(response, "/api/v1/categories/")
