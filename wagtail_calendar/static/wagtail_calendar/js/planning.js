$(document).ready(function() {
    // Get variables
    var $planning_calendar = $('#planning-calendar');
    var locale = $planning_calendar.attr('data-locale').substr(0, 2);
    var update_url = $planning_calendar.attr('data-update-url');
    var events_url = $planning_calendar.attr('data-events-url');
    var csrf_token = $planning_calendar.attr('data-csrf');

  // Initialize side events
  $('.side-events').draggable({
      zIndex: 999,
      revert: true,
      revertDuration: 0
  });

  var updateEvent = function(event) {
      var url = update_url.replace(0, event.data.pk);
      $.post(url, {
          go_live_at: event.start.format().replace('T', ' '),  // Django default datetime validation...
          csrfmiddlewaretoken: csrf_token
      });
  };

  var eventDrop = function(event, delta, revertFunc) {
      if (event.data.type === 'page' && event.data.pk !== undefined) {
          if (!event.start.hasTime()) {
              revertFunc();
          } else {
              updateEvent(event);
          }
      }
  };

  var eventReceive = function(event) {
      if (event.data.type === 'page' && event.data.pk !== undefined) {
          if (!event.start.hasTime()) {
              event.start.time(0);
              event.end = event.start.clone().add(2, 'hours');
              event.allDay = false;
              $planning_calendar.fullCalendar('updateEvent', event);
          }
          updateEvent(event);
          $('#side-event-'+ event.id).remove();
      }
  };

  $planning_calendar.fullCalendar({
      locale: locale,
      header: {
        left:   'title',
        center: 'month agendaWeek agendaDay',
        right:  'today prev,next'
      },
      droppable: true,
      events: events_url,
      eventDrop: eventDrop,
      eventReceive: eventReceive
  });
});