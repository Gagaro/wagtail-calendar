$(document).ready(function() {
    // Get variables
    var $planning_calendar = $('#planning-calendar');
    var locale = $planning_calendar.attr('data-locale').substr(0, 2);
    var update_url = $planning_calendar.attr('data-update-url');
    var events_url = $planning_calendar.attr('data-events-url');
    var csrf_token = $planning_calendar.attr('data-csrf');

  // Initialize side events
  $('.side-event-draggable').draggable({
      zIndex: 999,
      revert: true,
      revertDuration: 0
  });

  var updateEvent = function(event) {
      var url = update_url.replace(0, event.data.pk);

      $.post(url, {
          go_live_at: event.start ? event.start.format().replace('T', ' ') : null,  // Django default datetime validation...
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

  var isEventOverDropzone = function(x, y) {
      var external_events = $('#side-events-dropzone');
      var offset = external_events.offset();
      offset.right = external_events.width() + offset.left;
      offset.bottom = external_events.height() + offset.top;

      // Compare
      return x >= offset.left
          && y >= offset.top
          && x <= offset.right
          && y <= offset.bottom;
  };

  var eventDragStop = function(event, jsEvent, ui, view) {
      if (isEventOverDropzone(jsEvent.clientX, jsEvent.clientY)) {
          $planning_calendar.fullCalendar('removeEvents', event.id);
          var el = $("<div class='side-events fc-event' id='side-event-"+ event.id +"'>").appendTo('#side-events-dropzone').text(event.title);
          el.draggable({
              zIndex: 999,
              revert: true,
              revertDuration: 0
          });
          el.data('event', event);
          event.start = null;
          updateEvent(event);
      }
  };

  var $popup = $('div#event-popup');
  var eventClick = function(event, jsEvent, view) {
      var $event = $(this);
      var $titleLink = $('<a>', {text: event.title, href: event.url});
      $popup.find('#event-title').html('<i>(' + event.data.status + ')</i> ').append($titleLink);
      $popup.find('#event-author').text(event.data.author);
      $popup.find('#event-description').html(event.data.description);
      $popup.show();
      // Position need to be calculated when the popup is visible
      $popupParent = $popup.offsetParent();
      var top = $event.offset().top - $popupParent.offset().top + $event.height();
      var left = $event.offset().left - $popupParent.offset().left;
      $popup.css({top: top, left: left});
      return false;
  };

  $popup.find('#event-popup-close').click(function(event) {
      event.preventDefault();
      $popup.hide();
  });

  $planning_calendar.fullCalendar({
      locale: locale,
      header: {
        left:   'title',
        center: 'month agendaWeek agendaDay',
        right:  'today prev,next'
      },
      droppable: true,
      dragRevertDuration: 0,
      events: events_url,
      eventDrop: eventDrop,
      eventReceive: eventReceive,
      eventDragStop: eventDragStop,
      eventClick: eventClick
  });
});