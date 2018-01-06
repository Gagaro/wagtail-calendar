from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from wagtail.wagtailcore.hooks import get_hooks

from wagtail_calendar.tests.utils import TestEventsMixin


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
