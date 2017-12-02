from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.utils import timezone
from wagtail.wagtailcore.hooks import get_hooks
from wagtail.wagtailcore.models import Page


class TestEventsMixin(object):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='test_user')
        cls.published_page = Page.objects.create(
            owner=cls.user,
            slug='published',
            title='published',
            path='00010002',
            depth=2,
        )
        cls.published_page.save_revision(user=cls.user)
        revision = cls.published_page.save_revision(user=cls.user)
        revision.publish()

        cls.planned_page = Page.objects.create(
            owner=cls.user,
            go_live_at=timezone.now(),
            slug='planned',
            title='planned',
            path='00010003',
            depth=2,
        )
        cls.planned_page.save_revision(user=cls.user)
        cls.planned_page.save_revision(user=cls.user)

        cls.unplanned_page = Page.objects.create(
            owner=cls.user,
            slug='unplanned',
            title='unplanned',
            path='00010004',
            depth=2,
        )
        cls.unplanned_page.save_revision(user=cls.user)
        cls.unplanned_page.save_revision(user=cls.user)

    def setUp(self):
        self.request_factory = RequestFactory()


class TestRegisterEvent(TestEventsMixin, TestCase):

    def _get_events(self, start, end):
        request = self.request_factory.get('/')
        request.user = self.user
        events = []
        for hook in get_hooks('wagtail_calendar_register_events'):
            events = hook(request, start, end, events)
        return events

    def _get_event_ids(self, start=None, end=None):
        if start is None:
            start = timezone.now() - timedelta(days=15)
        if end is None:
            end = timezone.now() + timedelta(days=15)
        events = self._get_events(start.isoformat(), end.isoformat())
        return [event['id'] for event in events]

    def test_there_is_no_duplicated_events(self):
        self.assertEqual(len(self._get_event_ids()), 2)

    def test_published_page_in_hook(self):
        self.assertIn(self.planned_page.id, self._get_event_ids())

    def test_planned_page_in_hook(self):
        self.assertIn(self.published_page.id, self._get_event_ids())

    def test_unplanned_page_not_in_hook(self):
        self.assertNotIn(self.unplanned_page.id, self._get_event_ids())


class TestRegisterSideEvent(TestEventsMixin, TestCase):

    def _get_events(self):
        request = self.request_factory.get('/')
        request.user = self.user
        events = []
        for hook in get_hooks('wagtail_calendar_register_side_events'):
            events = hook(request, events)
        return events

    def _get_event_ids(self):
        events = self._get_events()
        return [event['id'] for event in events]

    def test_there_is_no_duplicated_events(self):
        self.assertEqual(len(self._get_event_ids()), 1)

    def test_published_page_not_in_hook(self):
        self.assertNotIn(self.planned_page.id, self._get_event_ids())

    def test_planned_page_not_in_hook(self):
        self.assertNotIn(self.published_page.id, self._get_event_ids())

    def test_unplanned_page_in_hook(self):
        self.assertIn(self.unplanned_page.id, self._get_event_ids())
