# Coffee for information.html

jQuery ->
    # Initialize date / time pickers
    $('#startDate, #endDate').parent().datepicker()
    $('#startTime, #endTime').timepicker
        minuteStep: 5
    
    # Initialize tooltips
    $('label[rel="tooltip"]').tooltip()
    
    # Form validation
    $('#election-submit').click(submitForm)

# Called when the submit button is clicked. Validates & makes an AJAX call.
submitForm = ->
    # Validate
    postData =
        'name': getElectionName()
        'start': getElectionTimes()['start']
        'end': getElectionTimes()['end']
        'result_delay': getResultDelay()
        'universal': isUniversalElection()

    for key, value of postData
        if value == null
            scrollToTop()
            return false

    $.ajax
        url: '/admin/organization-panel/election-panel/information'
        type: 'POST'
        data: 'formData': JSON.stringify(postData)
        success: (data) ->
            response = JSON.parse(data)
            setButton('btn-success', response['msg'])
        error: (data) ->
            setButton('btn-danger', 'Error')

setButton = (type, text) ->
    btn = $('#election-submit')
    btn.attr('class', 'btn')
    btn.addClass(type)
    btn.text(text)

scrollToTop = ->
    $('html, body').animate scrollTop: $('#createForm').offset().top, 500

getElectionName = ->
    name = $('#name')
    nameContainer = name.parent().parent()
    nameContainer.removeClass('error')
    $('.errorMsgName').remove()
    if not name.val()
        nameContainer.addClass('error')
        $("<span class='help-inline errorMsgName'>Please enter election " +
            "name.</span>").insertAfter(name)
        return null
    return name.val()

getElectionTimes = ->
    startDate = $('#startDate')
    startTime = $('#startTime')
    endDate = $('#endDate')
    endTime = $('#endTime')
    timeContainer = startDate.parent().parent().parent()
    errorMsg = ''
    for field in [startDate, startTime, endDate, endTime]
        errorMsg = 'Missing information.' if not field.val()
    
    if not errorMsg
        start = new Date("#{startDate.val()} #{startTime.val()}").getTime()
        end = new Date("#{endDate.val()} #{endTime.val()}").getTime()
        start /= 1000
        end /= 1000
        if start > end
            errorMsg = 'Start time is later than end time.'
        if start == end
            errorMsg = 'Start time is the same as end time.'
    
    if errorMsg
        timeContainer.addClass('error')
        $('.errorMsgTime').remove()
        startDate.parent().parent().append("<span class='help-inline " +
            "errorMsgTime'>#{errorMsg}</span>")
        return null
    else
        timeContainer.removeClass('error')
        $('.errorMsgTime').remove()
        return 'start': start, 'end': end
            
getResultDelay = -> parseInt($('#result-delay').val())

isUniversalElection = -> $('#universal-election').attr('checked') == 'checked'