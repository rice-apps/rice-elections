/**
 * Loading this adjusts all times with tag class 'date' to the user's local time zone.
 */
$(document).ready(function() {
    $('.date-format').each(function() {
        var date = Date.parse($(this).text());
        var dateOb = new Date(date);
        var newDateStr = dateOb.toString().substring(0, 15);
        var newTimeStr = dateOb.toLocaleTimeString();
        var len = dateOb.toString().length;
        var newTimeZoneStr = dateOb.toString().substring(len-4, len-1);
        var out = newDateStr + ', ' + newTimeStr;
        $(this).text(out);
    });
});
