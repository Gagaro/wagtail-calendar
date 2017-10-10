from django.conf.urls import url, include
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from wagtail.wagtailadmin.menu import MenuItem
from wagtail.wagtailcore import hooks

from wagtail_calendar import urls


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
