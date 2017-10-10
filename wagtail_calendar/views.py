from django.http import JsonResponse
from django.views.generic import TemplateView

from wagtail_calendar.utils import get_published_events, get_planned_events


class PlanningCalendarView(TemplateView):
    template_name = 'wagtail_calendar/planning_calendar.html'


def planning_calendar_events(request):
    start = request.GET.get('start', None)
    end = request.GET.get('end', None)

    pages = get_published_events(start, end, request) + get_planned_events(start, end, request)
    return JsonResponse(pages, safe=False)
