
var countdowns;
var time_on_page;

/**
 * Initializes JS event listeners on the page.
 */
$(document).ready(function() {
    startCountDownTimers()
    setInterval(function(){ countdown(); }, 1000);
});

function startCountDownTimers() {
    countdowns = $('.countdown')
    time_on_page = 0;
}

function countdown() {
    var time_left;
    time_on_page += 1000;
    $.each(countdowns, function(i, countdown) {
        time_left = $(this).attr('data-time-remaining')
        $(this).html(getTimerFromMilliseconds(time_left - time_on_page))
        if (time_left - time_on_page < 0) {
            $(this).removeClass('countdown')
            $(this).removeClass('disabled')
            $(this).html($(this).attr('data-countdown-over-text'))
            $(this).attr('href', $(this).attr('data-href'))
        }
    });
}

function getTimerFromMilliseconds(millis){
    var hours = Math.floor(millis / 36e5),
        mins = Math.floor((millis % 36e5) / 6e4),
        secs = Math.floor((millis % 6e4) / 1000);
    if (mins < 10)
        mins = 0 + "" + mins;
    if (secs < 10)
        secs = 0 + "" + secs;
    if (hours < 10)
        hours = 0 + "" + hours;
    return hours+':'+mins+':'+secs
}