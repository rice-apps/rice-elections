# JS for election panel positions.html

# Positions added in the election where each position is an object literal
all_positions = []
rankedModal = null
cumulativeModal = null
form = null

jQuery ->
    rankedModal = new RankedVotingPosition()
    cumulativeModal = new CumulativeVotingPosition()
    form = new Form()

# Form for managing positions
Form = ->
    @positions = []

    Form::processPosition = (position) ->
        if not position['pageId']
            position['pageId'] = @positions.length
        @positions[position['pageId']] = position
        createPositionHTML(position)

    createPositionHTML = (position) ->
        id = position['pageId']
        html = $("
        <tr id='position-#{id}' style='padding-bottom:5px;'>
            <td>
                <i class='icon-user'></i> #{position['name']}
            </td>
            <td>
                <a href='#' id='position-#{id}-edit'>Edit</a> &middot;
                <a href='#' class='delete-position' id='position-#{id}-delete'>Delete</a>
            </td>
        </tr>
        ")
        $('#positions').append(html)
        $('#no-positions').hide()
        html.hide().slideDown(500)

    return # Stops compiler from returning last defined function


# Abstract base class different position types, replace type in subclasses
Position = (type) ->
    # Closure reference
    self = this

    # Position ID for page reference
    @pageId = null

    # Datastore entity ID
    @entityId = null

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

    # Submit button for the modal
    @submit = $("#modal-#{@type}-submit")

    # Gives the contents of the form in json form if valid, otherwise null
    Position::toJson = ->
        position =
            'pageId': @pageId
            'entityId': @entityId
        return position

    # Resets the HTML form
    Position::reset = ->
        @candidateIDs = []
        @candidates.children().remove()
        @name.val('').change()
        @voteRequired.attr('checked', false)

    # Validates and adds / updates the modal
    @submit.click (e) =>
        json = @toJson()
        return false if json == null
        $("#modal-#{@type}").modal('hide')
        @reset()
        form.processPosition(json)

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
            if nameInput.val() == ''
                missing = true
            else
                canList.push(nameInput.val())

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
        if @candidateIDs.length == 0 and val == 0
            slotsContainer.addClass('error')
            $('<span class="help-inline errorMsgSlots">Must have atleast a ' +
                'single write in slot if no candidates are specified.' +
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
        position = Position::toJson.call(this)
        json =
            'type': 'Ranked-Choice'
            'name': @getName()
            'candidates': @getCandidates()
            'write_in': @getWriteInSlots()
            'vote_required': @hasVoteRequirement()
        for key, value of json
            return null if value == null
            position[key] = value
        return position

    return # Stops compiler from returning last defined function

# Inherit from Position
RankedVotingPosition:: = new Position
RankedVotingPosition::constructor = RankedVotingPosition

CumulativeVotingPosition = ->
    Position.call(this, "cumulative")

    self = this

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
        position = Position::toJson.call(this)
        json =
            'type': 'Cumulative-Voting'
            'name': @getName()
            'candidates': @getCandidates()
            'write_in': @getWriteInSlots()
            'vote_required': @hasVoteRequirement()
            'slots': @getSlots()
            'points': @getPoints()
        for key, value of json
            return null if value == null
            position[key] = value
        return position

    return # Stops compiler from returning last defined function

# Inherit from Position
CumulativeVotingPosition:: = new Position
CumulativeVotingPosition::constructor = CumulativeVotingPosition

