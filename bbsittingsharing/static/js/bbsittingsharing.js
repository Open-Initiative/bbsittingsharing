function syncCalendars(view, element) {
    var moment = view.calendar.getDate().add(1, 'month');
    $('#calendar-right').fullCalendar('gotoDate', moment);
    $('#calendar-right').fullCalendar('changeView', 'month');
}

function selectDate(event, jsEvent, view) {
    console.log(event);
}
