from django.conf.urls import url

from wagtail_calendar.views import PlanningCalendarView, planning_calendar_events

urlpatterns = [
    url(r'^$', PlanningCalendarView.as_view(), name='planning_calendar'),
    url(r'^events/$', planning_calendar_events, name='planning_calendar_events'),
]
