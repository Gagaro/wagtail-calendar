from django.contrib.auth.models import User
from django.test import RequestFactory
from django.utils import timezone
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
