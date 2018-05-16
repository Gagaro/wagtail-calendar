from django.conf.urls import url, include
from django.urls import reverse
from django.utils.dateparse import parse_datetime
from django.utils.translation import ugettext_lazy as _
from wagtail.wagtailadmin.menu import MenuItem
from wagtail.wagtailcore import hooks
from wagtail.wagtailcore.models import Page, PageRevision, UserPagePermissionsProxy

from wagtail_calendar import urls
from wagtail_calendar.utils import get_page_event_data


@hooks.register('register_admin_urls')
def register_admin_urls():
    return [
        url(r'^calendar/', include(urls, namespace='wagtail_calendar')),
    ]


@hooks.register('register_admin_menu_item')
def register_styleguide_menu_item():
    return MenuItem(
        _('Calendar'),
        reverse('wagtail_calendar:planning_calendar'),
        classnames='icon icon-date',
        order=1000
    )


@hooks.register('wagtail_calendar_register_events')
def register_published_events(request, start, end, events):
    permissions = UserPagePermissionsProxy(request.user)
    queryset = Page.objects.filter(first_published_at__isnull=False)
    if start is not None:
        queryset = queryset.filter(first_published_at__gte=start)
    if end is not None:
        queryset = queryset.filter(first_published_at__lte=end)
    queryset = queryset.specific()
    return events + [
        {
            'id': page.pk,
            'title': page.title,
            'start': page.first_published_at.isoformat(),
            'url': page.get_url(request),
            'editable': permissions.for_page(page).can_unpublish(),
            'color': '#333',
            'data': get_page_event_data(page),
        }
        for page in queryset
    ]


@hooks.register('wagtail_calendar_register_events')
def register_planned_events(request, start, end, events):
    permissions = UserPagePermissionsProxy(request.user)
    # Only get the last revision of never published and planned pages
    queryset = (
        PageRevision.objects
        .filter(page__first_published_at__isnull=True)
        .order_by('page', '-created_at')
        # .distinct('page')  # Doesn't work with sqlite
    )
    if start is not None:
        start = parse_datetime(start)
    if end is not None:
        end = parse_datetime(end)
    pages = []
    ids = set()
    for page in queryset:
        page = page.as_page_object()
        if page.go_live_at is None:
            continue
        if start is not None and start > page.go_live_at:
            continue
        if end is not None and end < page.go_live_at:
            continue
        if page.pk in ids:
            continue  # Avoid duplicated event
        # Determine event color
        color = '#e9b04d'
        if page.expired:
            color = '#f37e77'
        elif page.approved_schedule:
            color = '#358c8b'
        ids.add(page.pk)
        pages.append({
            'id': page.pk,
            'title': page.title,
            'start': page.go_live_at.isoformat(),
            'url': page.get_url(request),
            'editable': permissions.for_page(page).can_publish(),
            'color': color,
            'data': get_page_event_data(page),
        })
    return events + pages


@hooks.register('wagtail_calendar_register_side_events')
def register_unplanned_events(request, events):
    permissions = UserPagePermissionsProxy(request.user)
    # Only get the last revision of never published and unplanned pages
    queryset = (
        PageRevision.objects
        .filter(page__first_published_at__isnull=True)
        .order_by('page', '-created_at')
        # .distinct('page')  # Doesn't work with sqlite
    )
    pages = []
    ids = set()
    for page in queryset:
        page = page.as_page_object()
        if page.go_live_at is not None:
            continue
        if page.pk in ids:
            continue  # Avoid duplicated event
        ids.add(page.pk)
        pages.append({
            'id': page.pk,
            'title': page.title,
            'url': page.get_url(request),
            'editable': permissions.for_page(page).can_publish(),
            'color': '#e9b04d',
            'stick': True,
            'data': get_page_event_data(page),
        })
    return events + pages
