from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.chapters.models import Chapter
from apps.core.choices import PublicationStatus
from apps.core.testing import make_chapter, make_fanfic, make_user


class ChapterModelTests(TestCase):
    def setUp(self):
        self.fanfic = make_fanfic()

    def test_draft_can_be_saved_without_publication_date(self):
        chapter = make_chapter(self.fanfic, status=PublicationStatus.DRAFT)
        self.assertIsNone(chapter.published)

    def test_publish_sets_date_and_unpublish_clears_it(self):
        chapter = make_chapter(self.fanfic, status=PublicationStatus.DRAFT)
        chapter.publish()
        self.assertIsNotNone(chapter.published)
        chapter.unpublish()
        self.assertIsNone(chapter.published)

    def test_order_is_numbered_per_fanfic(self):
        first = make_chapter(self.fanfic)
        second = make_chapter(self.fanfic)
        other = make_chapter(make_fanfic())
        self.assertEqual((first.order, second.order, other.order), (0, 1, 0))

    def test_empty_text_is_rejected(self):
        with self.assertRaises(ValidationError):
            make_chapter(self.fanfic, text="   ")

    def test_visible_to(self):
        author = self.fanfic.author
        published = make_chapter(self.fanfic)
        draft = make_chapter(self.fanfic, status=PublicationStatus.DRAFT)
        hidden_fanfic = make_fanfic(author, status=PublicationStatus.DRAFT)
        in_draft_fanfic = make_chapter(hidden_fanfic)

        self.assertEqual(list(Chapter.objects.visible_to(None)), [published])
        self.assertEqual(list(Chapter.objects.visible_to(make_user())), [published])
        self.assertCountEqual(
            Chapter.objects.visible_to(author), [published, draft, in_draft_fanfic]
        )
