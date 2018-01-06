from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from wagtail.tests.utils import WagtailTestUtils
from wagtail.wagtailcore.models import Page

from wagtail_calendar.tests.utils import TestEventsMixin


class TestPlanningCalendarView(TestEventsMixin, WagtailTestUtils, TestCase):
    def setUp(self):
        self.login()

    def test_get(self):
        response = self.client.get(reverse('wagtail_calendar:planning_calendar'))
        self.assertTemplateUsed(response, 'wagtail_calendar/planning_calendar.html')


class TestPlanningCalendarEventsView(TestEventsMixin, WagtailTestUtils, TestCase):
    def setUp(self):
        self.login()

    def test_get(self):
        year = timezone.now().year
        start = '{0}-01-01'.format(year)
        end = '{0}-01-01'.format(year + 1)
        url = '{0}?start={1}&end={2}'.format(reverse('wagtail_calendar:planning_calendar_events'), start, end)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)


class TestChangePagePlanningView(TestEventsMixin, WagtailTestUtils, TestCase):
    def setUp(self):
        self.login()

    def test_plan_page(self):
        url = reverse('wagtail_calendar:planning_calendar_plan_page', kwargs={'pk': self.unplanned_page.pk})
        response = self.client.post(url, {'go_live_at': '2016-11-05 00:00:00'})
        self.assertEqual(response.status_code, 200)
        page = Page.objects.get(pk=self.unplanned_page.pk)
        self.assertEqual(page.get_latest_revision_as_page().go_live_at.year, 2016)

    def test_unplan_page(self):
        url = reverse('wagtail_calendar:planning_calendar_plan_page', kwargs={'pk': self.planned_page.pk})
        response = self.client.post(url, {'go_live_at': ''})
        self.assertEqual(response.status_code, 200)
        page = Page.objects.get(pk=self.planned_page.pk)
        self.assertEqual(page.get_latest_revision_as_page().go_live_at, None)

    def test_change_page_planning(self):
        url = reverse('wagtail_calendar:planning_calendar_plan_page', kwargs={'pk': self.planned_page.pk})
        response = self.client.post(url, {'go_live_at': '2016-11-05 00:00:00'})
        self.assertEqual(response.status_code, 200)
        page = Page.objects.get(pk=self.planned_page.pk)
        self.assertEqual(page.get_latest_revision_as_page().go_live_at.year, 2016)
