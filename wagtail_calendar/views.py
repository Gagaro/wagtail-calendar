from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.views.generic.edit import BaseUpdateView
from wagtail.wagtailadmin.edit_handlers import get_form_for_model
from wagtail.wagtailcore.hooks import get_hooks
from wagtail.wagtailcore.models import Page


class PlanningCalendarView(TemplateView):
    template_name = 'wagtail_calendar/planning_calendar.html'

    def get_unplanned_events(self):
        events = []
        for hook in get_hooks('wagtail_calendar_register_side_events'):
            events = hook(self.request, events)
        return events

    def get_context_data(self, **kwargs):
        context = super(PlanningCalendarView, self).get_context_data(**kwargs)
        context['unplanned_events'] = self.get_unplanned_events()
        return context


def planning_calendar_events(request):
    start = request.GET.get('start', None)
    end = request.GET.get('end', None)

    events = []
    for hook in get_hooks('wagtail_calendar_register_events'):
        events = hook(request, start, end, events)
    return JsonResponse(events, safe=False)


class ChangePagePlanning(BaseUpdateView):
    http_method_names = ['post']
    queryset = Page.objects

    def get_object(self, queryset=None):
        return self.get_queryset().get(pk=self.kwargs['pk']).get_latest_revision_as_page()

    def get_form_class(self):
        content_type = ContentType.objects.get_for_model(self.object)
        page_class = content_type.model_class()
        return get_form_for_model(page_class, fields=['go_live_at'], formsets=[])

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.permissions_for_user(request.user).can_publish():
            raise PermissionDenied
        return super(ChangePagePlanning, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        page = form.save(commit=False)
        page.save_revision(user=self.request.user)
        return JsonResponse({'status': 'ok'})

    def form_invalid(self, form):
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
