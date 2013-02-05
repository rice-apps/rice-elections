# Coffee for information.html

jQuery ->
    informationForm = new InformationForm()

    # Get election information from the server
    $.ajax
        url: '/admin/organization-panel/election-panel/information'
        type: 'POST'
        success: (data) ->
            response = JSON.parse(data)
            if response['status'] == 'ERROR'
                console.log('User not authorized')
                return
            if response['election']
                console.log(response['election'])
                informationForm.setFromJson(response['election'])
                informationForm.resetSubmitBtn()
        error: (data) ->
            console.log('Unknown Error')


# Class for an information form
InformationForm = ->
    # Closure reference
    self = this

    # String: the Datastore id of the election
    @id = ""

    # Input: Election Name
    @name = $('#name')

    # Start Date Picker
    @startDate = $('#startDate')

    # End Date Picker
    @endDate = $('#endDate')

    # Start Time Picker
    @startTime = $('#startTime')

    # End Time Picker
    @endTime = $('#endTime')

    # Input Choice: The delay in results to public
    @resultDelay = $('#result-delay') 

    # Checkbox: Whether the election is universal
    @universal = $('#universal-election')

    # Submit Button
    @submitBtn = $('#election-submit')

    # Initialize date / time pickers
    $('#startDate, #endDate').parent().datepicker()
    $('#startTime, #endTime').timepicker
        minuteStep: 5
        defaultTime: 'current'
        template: 'dropdown'

    # Called when the submit button is clicked. Validates & makes an AJAX call.
    @submitBtn.click ->
        return false if self.submitBtn.hasClass('disabled')
        postData = self.toJson()

        return false if not postData
        
        self.submitBtn.addClass('disabled')

        $.ajax
            url: '/admin/organization-panel/election-panel/information/update'
            type: 'POST'
            data: 'formData': JSON.stringify(postData)
            success: (data) ->
                response = JSON.parse(data)
                self.setSubmitBtn('btn-success', response['msg'])
            error: (data) ->
                self.setButton('btn-danger', 'Error')
        return true

    # Gives the contents of the form in json form if valid, otherwise null
    InformationForm::toJson = ->
        json =
            'name': @getName()
            'times': @getTimes()
            'result_delay': @getResultDelay()
            'universal': @isUniversal()
        for key, value of json
            return null if value == null
        return json

    # Sets the contents of the form with the given json information
    InformationForm::setFromJson = (json) ->
        return if not json
        @id = json['id']
        @name.val(json['name'])
        start = json['times']['start']
        end = json['times']['end']
        @startDate.parent().datepicker('setValue', start)
        @startTime.timepicker('setTime',
                              start[start.length - 8 .. start.length])
        @endDate.parent().datepicker('setValue', end)
        @endTime.timepicker('setTime',
                            end[end.length - 8 .. end.length])

        # Set result delay
        delay = json['result_delay']
        if not $("#result-delay option[value=#{delay}]")
            @resultDelay.append(
                "<option id='custom' value='#{delay}'>#{delay}</option>")
        @resultDelay.val(delay).change()

        # Set universal election
        @universal.attr('checked', json['universal'] == true)


    # Resets the submit button ready for use
    InformationForm::resetSubmitBtn = ->
        text = 'Submit'
        if @id
            text = 'Update'
        self.setSubmitBtn('btn-primary', text)
        self.submitBtn.removeClass('disabled')


    # Sets the submit button to the specified message
    InformationForm::setSubmitBtn = (type, text) ->
        disabled = true if @submitBtn.hasClass('disabled')
        @submitBtn.attr('class', 'btn')     # Wipe all btn classes
        @submitBtn.addClass('disabled') if disabled
        @submitBtn.addClass(type)
        @submitBtn.text(text)

    # Validates and returns the election name
    InformationForm::getName = ->
        nameContainer = @name.parent().parent()
        nameContainer.removeClass('error')
        $('.errorMsgName').remove()
        if not @name.val()
            nameContainer.addClass('error')
            $("<span class='help-inline errorMsgName'>Please enter election " +
                "name.</span>").insertAfter(@name)
            return null
        return @name.val()

    # Validates and returns the election times
    InformationForm::getTimes = ->
        timeContainer = @startDate.parent().parent().parent()
        errorMsg = ''
        for field in [@startDate, @startTime, @endDate, @endTime]
            errorMsg = 'Missing information.' if not field.val()
        
        if not errorMsg
            start = new Date("#{@startDate.val()} #{@startTime.val()}").getTime()
            end = new Date("#{@endDate.val()} #{@endTime.val()}").getTime()
            start /= 1000
            end /= 1000
            if start > end
                errorMsg = 'Start time is later than end time.'
            if start == end
                errorMsg = 'Start time is the same as end time.'
        
        if errorMsg
            timeContainer.addClass('error')
            $('.errorMsgTime').remove()
            @startDate.parent().parent().append("<span class='help-inline " +
                "errorMsgTime'>#{errorMsg}</span>")
            return null
        else
            timeContainer.removeClass('error')
            $('.errorMsgTime').remove()
            return 'start': start, 'end': end
    
    # Returns the election result delay
    InformationForm::getResultDelay = -> parseInt(@resultDelay.val())

    # Returns whether the election is universal
    InformationForm::isUniversal = -> @universal.attr('checked') == 'checked'

    # Trigger reset buttons on value changes
    for item in [@name, @resultDelay, @universal]
        item.change(@resetSubmitBtn)

    for picker in [@startTime, @endTime]
        picker.timepicker().on('changeTime.timepicker', @resetSubmitBtn)

    for picker in [@startDate, @endDate]
        picker.parent().datepicker().on('changeDate', @resetSubmitBtn)

    return # Stops compiler from returning last defined function