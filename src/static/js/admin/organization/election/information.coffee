# Coffee for information.html
informationForm = null
postURL = '/admin/organization/election/information'
jQuery ->
    $('label[rel="tooltip"]').tooltip()
    informationForm = new InformationForm()

    data =
        'method': 'get_election'

    # Get election information from the server
    $.ajax
        url: postURL
        type: 'POST'
        data: 'data': JSON.stringify(data)
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
    @startDate = $('#startDate').datepicker()
        # # Can't pick a start date in the past
        # onRender: (date) ->
        #     if date.valueOf() >= now.valueOf() then '' else 'disabled'
    .on 'changeDate', (ev) =>
        if ev.date.valueOf() > @endDate.date.valueOf()
            newDate = new Date(ev.date)
            @endDate.setValue(newDate)
        @startDate.hide()
        @resetSubmitBtn
        @endDate.show()
    .data('datepicker')

    # End Date Picker
    @endDate = $('#endDate').datepicker()
        # onRender: (date) =>
        #     if date.valueOf() < @startDate.date.valueOf() then 'disabled' else ''
    .on 'changeDate', (ev) =>
        if ev.date.valueOf() > @pubDate.date.valueOf()
            newDate = new Date(ev.date)
            @pubDate.setValue(newDate)
        @endDate.hide()
        @resetSubmitBtn
        @pubDate.show()
    .data('datepicker')

    @pubDate = $('#pubDate').datepicker()
    .on 'changeDate', (ev) =>
        @pubDate.hide()
        @resetSubmitBtn
    .data('datepicker')

    $('#startTime, #endTime, #pubTime').timepicker
        minuteStep: 5
        defaultTime: 'current'
        template: 'dropdown'

    # Start Time Picker
    @startTime = $('#startTime')

    # End Time Picker
    @endTime = $('#endTime')

    # Pub Time Picker
    @pubTime = $('#pubTime')

    # Checkbox: Whether the election is universal
    @universal = $('#universal-election')

    # Warning: Displayed when the election is universal
    @universalWarning = $('#universal-election-warning')

    # Checkbox: Whether the election is hidden
    @hidden = $('#hidden-election')

    # Description
    @description = $('#description') 
    
    # Election link modal
    @linkModal = new LinkModal()

    # Submit Button
    @submitBtn = $('#election-submit')

    # Called when the submit button is clicked. Validates & makes an AJAX call.
    @submitBtn.click =>
        return false if self.submitBtn.hasClass('disabled')
        data = self.toJson()
        return false if not data

        data['method'] = 'update_election'
        self.submitBtn.addClass('disabled')

        $.ajax
            url: postURL
            type: 'POST'
            data: 'data': JSON.stringify(data)
            success: (data) =>
                response = JSON.parse(data)
                self.setFromJson(response['election'])
                self.setSubmitBtn('btn-success', response['msg'])
                self.submitBtn.addClass('disabled')
                console.log(response)
                if response.election.hidden
                    @linkModal.load(response.election.id)
                    @linkModal.show()
            error: (data) ->
                self.setSubmitBtn('btn-danger', 'Error')
        return true

    # Gives the contents of the form in json form if valid, otherwise null
    InformationForm::toJson = ->
        json =
            'name': @getName()
            'times': @getTimes()
            'universal': @isUniversal()
            'hidden': @hidden.prop('checked')
            'description': @getDescription()
        for key, value of json
            return null if value == null
        return json

    # Sets the contents of the form with the given json information
    InformationForm::setFromJson = (json) ->
        return if not json
        @id = json['id']
        @name.val(json['name'])
        start = new Date(json['times']['start'] + ' UTC')
        end = new Date(json['times']['end'] + ' UTC')
        pub = new Date(json['times']['pub'] + ' UTC')
        now = new Date()
        startTime = start.toLocaleTimeString()
        endTime = end.toLocaleTimeString()
        pubTime = pub.toLocaleTimeString()
        @description.val(json['description'])
        
        # Set date / time picker components
        @startDate.setValue(start)
        if now.valueOf() > start.valueOf()
            @startDate.onRender = (date) -> 'disabled'
        @startDate.update()

        @endDate.setValue(end)
        if now.valueOf() > end.valueOf()
            @endDate.onRender = (date) -> 'disabled'
        @endDate.update()

        @pubDate.setValue(pub)
        if now.valueOf() > end.valueOf()
            @pubDate.onRender = (date) -> 'disabled'
        @pubDate.update()

        @startTime.timepicker('setTime', startTime)
        @endTime.timepicker('setTime', endTime)
        @pubTime.timepicker('setTime', pubTime)

        # Set universal election
        @universal.prop('checked', json['universal'] == true)
        if json['universal']
            @universalWarning.show();
        else
            @universalWarning.hide();

        # Set hidden election
        @hidden.prop('checked', json['hidden'] == true)


    # Resets the submit button ready for use
    InformationForm::resetSubmitBtn = ->
        text = 'Create Election'
        if self.id
            text = 'Update Election'
        self.setSubmitBtn('btn-primary', text)
        self.submitBtn.removeClass('disabled')


    # Sets the submit button to the specified message
    InformationForm::setSubmitBtn = (type, text) ->
        self.restoreDefaultButtonState()
        @submitBtn.addClass(type)
        @submitBtn.text(text)

    InformationForm::restoreDefaultButtonState = ->
        @submitBtn.removeClass('btn-success')
        @submitBtn.removeClass('btn-danger')
        @submitBtn.removeClass('btn-primary')

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

    # Gets the description for a position
    InformationForm::getDescription = ->
        return @description.val()
        
    # Validates and returns the election times
    InformationForm::getTimes = ->
        timeContainer = $('#startDate').parent().parent()
        pubTimeContainer = $('#pubDate').parent().parent()
        startDateInput = @startDate.element.children().filter('input')
        endDateInput = @endDate.element.children().filter('input')
        pubDateInput = @pubDate.element.children().filter('input')
        errorMsg = ''
        for field in [startDateInput, endDateInput, pubDateInput, @startTime, @endTime, @pubTime]
            errorMsg = 'Missing information.' if not field.val()

        if not errorMsg
            start = new Date("#{startDateInput.val()} #{@startTime.val()}").valueOf()
            end = new Date("#{endDateInput.val()} #{@endTime.val()}").valueOf()
            pub = new Date("#{pubDateInput.val()} #{@pubTime.val()}").valueOf()
            start /= 1000
            end /= 1000
            pub /= 1000
            console.log('Start time ' + start + '/ End time: ' + end, '/ Pub time: ' + pub)
            if end > pub
                pubErrorMsg = 'Publish time is before end time.'
            if start > end
                errorMsg = 'Start time is later than end time.'
            if start == end
                errorMsg = 'Start time is the same as end time.'
            if not @id and ((new Date()).valueOf() / 1000) > start
                errorMsg = 'Start time is in the past.'

        if errorMsg
            timeContainer.addClass('error')
            $('.errorMsgTime').remove()
            @startDate.element.parent().append("<span class='help-inline " +
                "errorMsgTime'>#{errorMsg}</span>")

        if pubErrorMsg
            pubTimeContainer.addClass('error')
            $('.pubErrorMsgTime').remove()
            @pubDate.element.parent().append("<span class='help-inline " +
                "pubErrorMsgTime'>#{pubErrorMsg}</span>")

        if errorMsg or pubErrorMsg
            return null
        else
            timeContainer.removeClass('error')
            $('.errorMsgTime').remove()
            pubTimeContainer.removeClass('error')
            $('.pubErrorMsgTime').remove()
            return 'start': start, 'end': end, 'pub': pub

    # Returns whether the election is universal
    InformationForm::isUniversal = -> @universal.prop('checked')

    # Trigger reset buttons on value changes
    for item in [@name, @universal, @hidden]
        item.change(@resetSubmitBtn)

    for picker in [@startTime, @endTime, @pubTime]
        picker.timepicker().on('changeTime.timepicker', @resetSubmitBtn)

    @universal.change (e) ->
        if self.universal.prop('checked')
            self.universalWarning.show()
        else
            self.universalWarning.hide()

    return # Stops compiler from returning last defined function

class LinkModal
    constructor: ->
        @el = $('#modal-election-link')
        @link = $('#modal-election-link-text')
        @linkHref = ''
        @copyLink = $('#modal-election-link-copy')
        @clip = new ZeroClipboard(@copyLink, {moviePath: "/static/js/shared/ZeroClipboard.swf", text: 'Hello!'})

        @clip.on 'complete', (client, args) ->
            alert("Copied text to clipboard: #{args.text}")
        # @copyLink.click(@copy)

    load: (id) ->
        host = window.location.host
        @linkHref = "http://#{host}/vote/cast-ballot?id=#{id}"
        linkText = $('<a>', 'href': @linkHref).text(@linkHref)
        @link.text(@linkHref)
        @copyLink.attr('data-clipboard-text', @linkHref)
        @clip = new ZeroClipboard(@copyLink, {moviePath: "/static/js/shared/ZeroClipboard.swf", text: 'Hello!'})

    show: -> @el.modal('show')
