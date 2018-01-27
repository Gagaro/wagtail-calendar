Customize
=========

Changing the event data
-----------------------

You can add a `get_page_event_data` method to your page model to change the data used by the calendar.
The default data are:

.. code-block:: python

    return {
        'type': 'page',
        'pk': page.pk,
        'author': str(page.owner),
        'description': page.search_description,  # description can be HTML to allow more customization of the popup
    }


Adding events
-------------

There are two wagtail hooks available to add events. `wagtail_calendar_register_events` is used to add events to the calendar.
The properties of the events are the one from `fullcalendar <https://fullcalendar.io/docs/event_data/Event_Object/>`_.
The hook take the request, a start date, a end date and a list of events already in the calendar.
You must return the whole list of events which will appear in the calendar.

.. code-block:: python

    @hooks.register('wagtail_calendar_register_events')
    def my_events(request, start, end, events):
        if start is not None:
            start = parse_datetime(start)
        if end is not None:
            end = parse_datetime(end)
        my_events = []
        for event in MyEvent.objects.filter(start__gte=start, end__lte=end):
            my_events.append({
                'id': event.pk,
                'title': event.title,
                'start': event.start.isoformat(),
                'end': event.end.isoformat(),
                'url': event.get_absolute_url(),
                'editable': False,
                'color': '#ff0000',
            })
        return events + my_events


`wagtail_calendar_register_side_events` is used to add events to the sidebar of the calendar. It is used for events which are not planned yet.
The properties of the events are the one from `fullcalendar <https://fullcalendar.io/docs/event_data/Event_Object/>`_.
The hook take the request and a list of events already in the sidebar.
You must return the whole list of events which will appear in the sidebar.

.. code-block:: python

    @hooks.register('wagtail_calendar_register_side_events')
    def my_events(request, start, end, events):
        my_events = []
        for event in MyEvent.objects.filter(start__isnull=True):
            my_events.append({
                'id': event.pk,
                'title': event.title,
                'url': event.get_absolute_url(),
                'editable': True,
                'color': '#ff0000',
            })
        return events + my_events
