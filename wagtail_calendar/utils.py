from django.utils.dateparse import parse_datetime
from wagtail.wagtailcore.models import Page, PageRevision


def get_published_events(start, end, request=None):
    queryset = Page.objects.filter(first_published_at__isnull=False)
    if start is not None:
        queryset = queryset.filter(first_published_at__gte=start)
    if end is not None:
        queryset = queryset.filter(first_published_at__lte=end)
    queryset = queryset.specific()
    return [{
        'id': page.pk,
        'title': page.title,
        'start': page.first_published_at.isoformat(),
        'url': page.get_url(request),
        'editable': False,
        'color': '#333',
    } for page in queryset]


def get_planned_events(start, end, request=None):
    # Only get the last revision of never published pages
    queryset = (
        PageRevision.objects
            .filter(page__first_published_at__isnull=True)
            .order_by('page', '-created_at')
            .distinct('page')
    )
    if start is not None:
        start = parse_datetime(start)
    if end is not None:
        end = parse_datetime(end)
    pages = []
    for page in queryset:
        page = page.as_page_object()
        if page.go_live_at is None:
            continue
        if start is not None and start > page.go_live_at:
            continue
        if end is not None and end < page.go_live_at:
            continue
        pages.append({
            'id': page.pk,
            'title': page.title,
            'start': page.go_live_at.isoformat(),
            'url': page.get_url(request),
            'editable': True,
            'color': '#e9b04d',
        })
    return pages
