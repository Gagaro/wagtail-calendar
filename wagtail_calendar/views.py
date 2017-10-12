from django.http import JsonResponse
from django.views.generic import TemplateView
from wagtail.wagtailcore.hooks import get_hooks


class PlanningCalendarView(TemplateView):
    template_name = 'wagtail_calendar/planning_calendar.html'


def planning_calendar_events(request):
    start = request.GET.get('start', None)
    end = request.GET.get('end', None)

    events = []
    for hook in get_hooks('wagtail_calendar_register_events'):
        events = hook(request, start, end, events)
    return JsonResponse(events, safe=False)
