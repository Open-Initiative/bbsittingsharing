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
    var div = $("<div class='"+date.format()+"'>");
    div.addClass("calendar-day");
    if(this.calendar.getDate().month()!=date.month())
        div.addClass('other-month');
    div.html('<a href="/search?date='+ date.format() +'">'
        +'<div class="detail"><span>0</span> bbsittings</div>'+ date.format("D") +'</a>');
    div.appendTo(cell);
    return false;
}

function renderEvent(event, element) {
    var div = $("."+event.start.format());
    div.addClass("booked");
    var span = $(".detail span", div);
    span.text(parseInt(span.text())+1);
    return false;
}

function reloadWithGroup() {
    //Get url parameters
    if(location.search)
        var params = JSON.parse('{"' + decodeURI(location.search.substring(1)).replace(/"/g, '\\"').replace(/&/g, '","').replace(/=/g,'":"') + '"}');
    else
        var params = {};
    params.group = $('#id_groups').val();
    window.location = '//' + location.host + location.pathname + '?' + $.param(params);
}

$(function() {
    var tasdanimaux = $("#tasdanimaux");
    if ($(this).scrollTop() > 420) tasdanimaux.addClass("scrolled");
    $(document).scroll(function(e) {
        if ($(this).scrollTop() > 420) tasdanimaux.addClass("scrolled");
        else tasdanimaux.removeClass("scrolled");
    });
});
