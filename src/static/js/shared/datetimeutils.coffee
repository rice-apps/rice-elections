
#Pad given value to the left with "0"
addZero = (num) ->
  (if (num >= 0 and num < 10) then "0" + num else num + "")

# Format date in mm/dd/yyyy
formatDate = (date) ->
  [addZero(date.getMonth() + 1), addZero(date.getDate()), date.getFullYear().toString().substring(2,4)].join "/"

###
Loading this adjusts all times with tag class 'date' to the user's local time zone.
###
$(document).ready ->
  $(".date-format").each ->
    date = Date.parse($(this).text())
    dateOb = new Date(date)
    newDateStr = dateOb.toString().substring(0, 15)
    newTimeStr = dateOb.toLocaleTimeString()
    len = dateOb.toString().length
    newTimeZoneStr = dateOb.toString().substring(len - 4, len - 1)
    out = newDateStr + ", " + newTimeStr
    $(this).text out