function syncCalendars(view, element) {
    var moment = view.calendar.getDate().add(1, 'month');
    $('#calendar-right').fullCalendar('gotoDate', moment);
    $('#calendar-right').fullCalendar('changeView', 'month');
}

function stepCalendar(step) {
    var moment = $('#calendar-left').fullCalendar('getDate').add(step, 'month');
    $('#calendar-left').fullCalendar('gotoDate', moment);
    $('#calendar-left').fullCalendar('changeView', 'month');
}

function renderDay(date, cell) {
    var div = $("<div id='"+date.format()+"'>");
    div.addClass("calendar-day");
    div.html('<a href="/search?date='+ date.format() +'">'+ date.format("D") +'</a>');
    div.appendTo(cell);
    return false;
}

function renderEvent(event, element) {
    var div = $("#"+event.start.format());
    div.addClass("booked");
    return false;
}

$(function() {
    var tasdanimaux = $("#tasdanimaux");
    $(document).scroll(function(e) {
        if ($(this).scrollTop() > 70) tasdanimaux.addClass("scrolled");
        else tasdanimaux.removeClass("scrolled");
    });
});
