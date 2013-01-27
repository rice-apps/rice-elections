# JS for create-election.html

jQuery ->
    # Initialize date / time pickers
    $('#startDate, #endDate').parent().datepicker()
    $('#startTime, #endTime').timepicker
        minuteStep: 5
    
    # Initialize tooltips
    $('label[rel="tooltip"]').tooltip()
    
    # Form validation
    $('#election-submit').click(submitForm)
    $('#createForm').bind 'reset', ->
        currentModal.resetForm()
        all_positions = []
        $('#positions-list').children().remove()


# Positions added in the election where each position is an object literal
all_positions = []

# Called when the submit button is clicked. Validates & makes an AJAX call.
submitForm = ->
    # Validate
    return false if $('#election-submit').hasClass('disabled')
    valid = true
    formData = [getElectionName(), getElectionTimes(), getEligibleVoters(),
        getPositions(), getResultDelay()]
    $.each formData, (index, value) -> valid = false if not value
    if not valid
        scrollToTop()
        return false
    
    postData =
        'name': formData[0]
        'start': formData[1]['start']
        'end': formData[1]['end']
        'voters': formData[2]
        'positions': formData[3]
        'result_delay': formData[4]
        'universal': isUniversalElection()

    $.ajax
        url: '/create-election'
        type: 'POST'
        data: 'formData': JSON.stringify(postData)
        success: (data) ->
            response = JSON.parse(data)
            scrollToTop()
            $('#server-response').addClass('alert')
            if response['status'] == 'OK'
                $('#server-response').addClass('alert-success')
            else
                $('#server-response').addClass('alert-error')
            $('#server-response').html(response['msg'])
            $('#server-response').hide().slideDown(1000)

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

getEligibleVoters = ->
    voters = $('#eligible-voters')
    votersContainer = voters.parent().parent()
    votersList = []
    for voter in voters.val().split(',')
        if voter.trim()
            votersList.push(voter.trim())
    votersContainer.removeClass('error')
    $('.errorMsgEligibleVoters').remove()
    if votersList.length == 0
        votersContainer.addClass('error')
        $("<span class='help-inline errorMsgEligibleVoters'>Missing " +
            "information.</span>").insertAfter(voters)
        return null
    return votersList

isUniversalElection = -> $('#universal-election').attr('checked') == 'checked'

getPositions = ->
    pos = $('#positions-list')
    posContainer = pos.parent().parent()
    posContainer.removeClass('error')
    $('.errorMsgPositions').remove()
    if all_positions.length == 0
        posContainer.addClass('error')
        $("<span class='help-inline errorMsgPositions'>Need at least one " +
            "position.</span>").insertAfter(pos);
        return null
    return all_positions

displayPosition = (position) ->
    html = "<div style='margin: 5px 0 5px;'><strong>#{position['type']}: " +
            "</strong>#{position['name']}<br /><ul>"
    for candidate in position['candidates']
        html += "<li>#{candidate['name']}: #{candidate['netId']}</li>"
    if position['vote_required']
        html += "<li><em>Vote required</em></li>"
    if position['slots']
        html += "<li><em>Position slots: #{position['slots']}</em></li>"
    if position['points']
        html += "<li><em>Points per voter: #{position['points']}</em></li>"
    html += "<li><em>Write-in Slots: #{position['write_in']}</em></li>"
    html += "</ul>"
    newPos = $(html)
    $('#positions-list').append(newPos)
    newPos.hide().slideDown(1000)


# Abstract base class different position types, replace type in subclasses
Position = (type) ->
    # Closure reference
    self = this

    # Position type
    @type = type

    # Generator for candidate IDs
    @candidateIDGen = 0
    
    # List of HTML IDs of candidates added to the form
    @candidateIDs = []
    
    # Generator for candidate IDs
    @candidateIDPrefix = "position-#{@type}-candidate-"
    
    # HTML ID prefix for candidates, 
    @addCandidate = $("#position-#{@type}-add-candidate")
    
    # Div: list of candidates
    @candidates = $("#position-#{@type}-candidates")

    # Text input: Position name input
    @name = $("#position-#{@type}-name")

    # Number input: Write-in slots
    @writeInSlots = $("#position-#{@type}-write-in")

    # Checkbox: Whether voting is required
    @voteRequired = $('#position-required')

    # Gives the contents of the form in json form if valid, otherwise null
    Position::toJson = ->
        throw new Error("Not implemented.")

    # Resets the HTML form
    Position::reset = ->
        @candidateIDs = []
        @candidates.children().remove()
        @name.val('').change()
        @voteRequired.attr('checked', false)

    # Adds an input field for a candidate to the form
    @addCandidate.click  ->
        index = self.candidateIDGen++
        id = self.candidateIDPrefix + index
        candidateInput = $('<div/>',
            class: 'input-append'
        ).append($('<input>',
            type: 'text'
            class: 'input-xlarge, input-margin-right'
            id: "#{id}-name"
            name: "#{id}-name"
            width: '200px'
            placeholder: 'Full Name'
        )).append($('<input>',
            type: 'text'
            class: 'input-xlarge'
            id: "#{id}-net-id"
            name: "#{id}-net-id"
            width: '50px'
            placeholder: 'NetID'
        )).append($('<span/>',
            class: 'add-on'
            id: "#{id}"
        ).append($('<i/>',
            class: 'icon-remove'
        )))
        self.candidates.append(candidateInput)
        candidateInput.hide().fadeIn(500)
        self.candidateIDs.push(index)
        
        # Delete candidate button
        $("##{id}").click ->
            indexPtr = self.candidateIDs.indexOf(index)
            self.candidateIDs.splice(indexPtr, 1) if indexPtr != -1
            $(this).parent().fadeOut(500)

    # Validates and returns the position name typed.
    Position::getName = ->
        nameContainer = @name.parent().parent()
        nameContainer.removeClass('error')
        $('.errorMsgPositionName').remove()
        if not @name.val()
            nameContainer.addClass('error')
            $('<span class="help-inline errorMsgPositionName">Missing ' +
                'information.</span>').insertAfter(@name)
            return null
        return @name.val()

    # Validates and returns a list of candidates
    Position::getCandidates = ->
        missing = false
        container = @candidates.parent().parent()
        canList = []    # Function output
        
        # Make sure the candidate name is defined for all candidates
        for can in @candidateIDs
            nameInput = $("#position-#{@type}-candidate-#{can}-name")
            netIdInput = $("#position-#{@type}-candidate-#{can}-net-id")
            if nameInput.val() == '' or netIdInput.val() == ''
                missing = true
            else
                canList.push(
                    'name': nameInput.val()
                    'netId': netIdInput.val()
                )
        
        $('.errorMsgCandidateName').remove()
        container.removeClass('error')
        if missing
            container.addClass('error')
            $('<span class="help-inline errorMsgSlots">Number of ' +
                'Missing information.</span>').insertAfter(@candidates)
            return null
        
        return canList

    # Validates and returns the write-in slots input number.
    Position::getWriteInSlots = ->
        slotsContainer = @writeInSlots.parent().parent()
        val = parseInt(@writeInSlots.val())
        min = parseInt(@writeInSlots.attr('min'))
        max = parseInt(@writeInSlots.attr('max'))
        slotsContainer.removeClass('error')
        $('.errorMsgSlots').remove()
        if not (min <= val and val <= max)
            slotsContainer.addClass('error')
            $('<span class="help-inline errorMsgSlots">Out of valid range.' +
                '</span>').insertAfter(@writeInSlots)
            return null
        return val

    # Whether voting is required for this position
    Position::hasVoteRequirement = -> @voteRequired.attr('checked') == 'checked'

    return # Stops compiler from returning last defined function

RankedVotingPosition = ->
    Position.call(this, "ranked")

    # Gives the contents of the form in json form if valid, otherwise null
    RankedVotingPosition::toJson = ->
        position =
            'type': 'Ranked-Choice'
            'name': @getName()
            'candidates': @getCandidates()
            'write_in': @getWriteInSlots()
            'vote_required': @hasVoteRequirement()
        for key, value of position
            return null if value == null
        return position

    return # Stops compiler from returning last defined function

# Inherit from Position
RankedVotingPosition:: = new Position
RankedVotingPosition::constructor = RankedVotingPosition

CumulativeVotingPosition = ->
    Position.call(this, "cumulative")

    # Number Input: Points
    @points = $('#position-cumulative-points')

    # Number Input: Position slots
    @slots = $('#position-cumulative-slots')

    # Validates and returns the points input number
    CumulativeVotingPosition::getPoints = ->
        pointsContainer = @points.parent().parent()
        val = parseInt(@points.val())
        min = parseInt(@points.attr('min'))
        max = parseInt(@points.attr('max'))
        pointsContainer.removeClass('error')
        $('.errorMsgSlots').remove()
        if not (min <= val and val <= max)
            pointsContainer.addClass('error')
            $('<span class="help-inline errorMsgSlots">Out of valid range.' +
                '</span>').insertAfter(@points)
            return null
        return val

    # Validates and returns the slot input number
    CumulativeVotingPosition::getSlots = ->
        slotsContainer = @slots.parent().parent()
        val = parseInt(@slots.val())
        min = parseInt(@slots.attr('min'))
        max = parseInt(@slots.attr('max'))
        slotsContainer.removeClass('error')
        $('.errorMsgSlots').remove()
        if not (min <= val and val <= max)
            slotsContainer.addClass('error')
            $('<span class="help-inline errorMsgSlots">Out of valid range.' +
                '</span>').insertAfter(@slots)
            return null
        else if (val > @candidateIDs.length and @getWriteInSlots() < 1)
            slotsContainer.addClass('error')
            $('<span class="help-inline errorMsgSlots">Number of ' +
                'slots exceed number of candidates.</span>').insertAfter(@slots)
            return null
        return val

    # Resets the HTML form
    CumulativeVotingPosition::reset = ->
        Position::reset.call(this)      # Call to super
        @slots.val('1').change()

    # Gives the contents of the form in json form if valid, otherwise null
    CumulativeVotingPosition::toJson = ->
        position =
            'type': 'Cumulative-Voting'
            'name': @getName()
            'candidates': @getCandidates()
            'write_in': @getWriteInSlots()
            'vote_required': @hasVoteRequirement()
            'slots': @getSlots()
            'points': @getPoints()
        for key, value of position
            return null if value == null
        return position

    return # Stops compiler from returning last defined function

# Inherit from Position
CumulativeVotingPosition:: = new Position
CumulativeVotingPosition::constructor = CumulativeVotingPosition

# A modal that guides the user through creating a position
addPositionModal = ->
    # Closure reference
    self = this

    # Drop-down: Position type
    @selectType = $("#position-select-type")
    
    # Divs: selected position types
    @selectionContent = $(".selection-content")
    
    # Ranked Voting Position instance
    @rankedVotingPosition = new RankedVotingPosition()

    # Cumulative Voting Position instance
    @cumulativeVotingPosition = new CumulativeVotingPosition()
    
    # Current position selected
    @positionSelected = @rankedVotingPosition

    # Submit Button
    @addSubmit = $('#position-add-submit');
    
    # Resets the HTML forms in the modal box on the page.
    addPositionModal::reset = -> 
        @selectType.val('0').change()
        @rankedVotingPosition.reset()
        @cumulativeVotingPosition.reset()
    
    # Updates the form when the position type is changed
    @selectType.change ->
        self.selectionContent.hide()
        selectionId = $(this).val()
        $("##{selectionId}").show()
        if selectionId == '0'
            self.positionSelected = self.rankedVotingPosition
        else
            self.positionSelected = self.cumulativeVotingPosition

    @addSubmit.click (e) =>
        position = @positionSelected.toJson()
        return false if position == null
        all_positions.push(position)
        displayPosition(position)
        $('#addPositions').modal('hide')
        @reset()
    
currentModal = new addPositionModal()
