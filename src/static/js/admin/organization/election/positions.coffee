# JS for election panel positions.html

# Positions added in the election where each position is an object literal
all_positions = []
rankedModal = null
cumulativeModal = null
form = null
postUrl = '/admin/organization/election/positions'

jQuery ->
    rankedModal = new RankedVotingPosition()
    cumulativeModal = new CumulativeVotingPosition()
    form = new Form()
    json = {'entityId': 'diwEVwjioxcWEq', 'write_in': 4, 'vote_required': true, 'name': 'Hello!', 'candidates': ['CanA', 'CanB', 'CanC']}

# Form for managing positions
class Form
    constructor: ->
        @positions = []

        # Load all of the existing positions into the form
        data =
            'method': 'get_positions'
        $.ajax
            url: postUrl
            type: 'POST'
            data: 
                'data': JSON.stringify(data)
            success: (data) =>
                response = JSON.parse(data)
                console.log(response)
                for position in response['positions']
                    @processPosition(position)
            error: (data) =>
                console.log('Unknown error')

    processPosition: (position) =>
        if not position['pageId']
            position['pageId'] = @positions.length
        @positions[position['pageId']] = position
        @createPositionHTML(position)

    createPositionHTML: (position) =>
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


# Abstract base class different position types, replace type in subclasses
class Position
    constructor: (@type) ->
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
        @voteRequired = $("#position-#{@type}-required")

        # Submit button for the modal
        @submit = $("#modal-#{@type}-submit")

        # Bind events
        @submit.click(@submitData)
        @addCandidate.click(@addCandidateSlot)

    # Gives the contents of the form in json form if valid, otherwise null
    toJson: =>
        position =
            'pageId': @pageId
            'entityId': @entityId
            'name': @getName()
            'candidates': @getCandidates()
            'write_in': @getWriteInSlots()
            'vote_required': @hasVoteRequirement()
        for key in ['name', 'candidates', 'write_in', 'vote_required']
            return null if position[key] == null
        return position

    setFromJson: (json) =>
        return if not json
        @reset()
        @entityId = json['entityId']
        @pageId = json['pageId']
        @writeInSlots.val(json['write_in'])
        @voteRequired.attr('checked', json['vote_required'])
        @name.val(json['name'])
        for candidate in json['candidates']
            @addCandidateSlot()
            index = @candidateIDGen - 1
            id = @candidateIDPrefix + index
            $("##{id}-name").val(candidate)

    # Resets the HTML form
    reset: =>
        @candidateIDs = []
        @candidates.children().remove()
        @name.val('').change()
        @voteRequired.attr('checked', false)

        # Remove all errors
        nameContainer = @name.parent().parent()
        nameContainer.removeClass('error')
        $('.errorMsgPositionName').remove()

        candidatesContainer = @candidates.parent().parent()
        $('.errorMsgCandidateName').remove()
        candidatesContainer.removeClass('error')

        slotsContainer = @writeInSlots.parent().parent()
        slotsContainer.removeClass('error')
        $('.errorMsgWSlots').remove()

    # Validates and adds / updates the modal
    submitData: (e) =>
        position = @toJson()
        return false if position == null

        data =
            'method': 'add_position'
            'position': position

        $.ajax
            url: postUrl
            type: 'POST'
            data:
                'data': JSON.stringify(data)
            success: (data) =>
                response = JSON.parse(data)
                if response['status'] == 'ERROR'
                    @setSubmitBtn('btn-danger', 'Error')
                    console.log("Error: #{response['msg']}")
                    return
                if response['status'] == 'OK'
                    $("#modal-#{@type}").modal('hide')
                    @reset()
                    form.processPosition(position)
            error: (data) =>
                @setSubmitBtn('btn-danger', 'Error')

    # Resets the submit button ready for use
    resetSubmitBtn: =>
        text = 'Create Position'
        if @entityId
            text = 'Update Position'
        @setSubmitBtn('btn-primary', text)
        @submit.removeClass('disabled')

    # Sets the submit button to the specified message
    setSubmitBtn: (type, text) =>
        @restoreDefaultButtonState()
        @submit.addClass(type)
        @submit.text(text)

    restoreDefaultButtonState: =>
        for cl in ['btn-success', 'btn-danger', 'btn-primary']
            @submit.removeClass(cl)

    # Adds an input field for a candidate to the form
    addCandidateSlot: =>
        index = @candidateIDGen++
        id = @candidateIDPrefix + index
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
        @candidates.append(candidateInput)
        candidateInput.hide().fadeIn(500)
        @candidateIDs.push(index)

        # Delete candidate button
        $("##{id}").click =>
            indexPtr = @candidateIDs.indexOf(index)
            @candidateIDs.splice(indexPtr, 1) if indexPtr != -1
            $("##{id}").parent().fadeOut(500)

    # Validates and returns the position name typed.
    getName: ->
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
    getCandidates: ->
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
            $('<span class="help-inline errorMsgCandidateName">' +
                'Missing information.</span>').insertAfter(@candidates)
            return null

        return canList

    # Validates and returns the write-in slots input number.
    getWriteInSlots: ->
        slotsContainer = @writeInSlots.parent().parent()
        val = parseInt(@writeInSlots.val())
        min = parseInt(@writeInSlots.attr('min'))
        max = parseInt(@writeInSlots.attr('max'))
        slotsContainer.removeClass('error')
        $('.errorMsgWSlots').remove()
        if not (min <= val and val <= max)
            slotsContainer.addClass('error')
            $('<span class="help-inline errorMsgWSlots">Out of valid range.' +
                '</span>').insertAfter(@writeInSlots)
            return null
        if @candidateIDs.length == 0 and val == 0
            slotsContainer.addClass('error')
            $('<span class="help-inline errorMsgWSlots">Must have atleast a ' +
                'single write in slot if no candidates are specified.' +
                '</span>').insertAfter(@writeInSlots)
            return null
        return val

    # Whether voting is required for this position
    hasVoteRequirement: -> @voteRequired.attr('checked') == 'checked'

class RankedVotingPosition extends Position
    constructor: ->
        super('ranked')

    # Gives the contents of the form in json form if valid, otherwise null
    toJson: =>
        position = super()
        return null if position == null
        position['type'] = 'Ranked-Choice'
        return position

    setFromJson: (json) =>
        super(json)

class CumulativeVotingPosition extends Position
    constructor: ->
        super('cumulative')

        # Number Input: Points
        @points = $('#position-cumulative-points')

        # Number Input: Position slots
        @slots = $('#position-cumulative-slots')

    # Validates and returns the points input number
    getPoints: ->
        pointsContainer = @points.parent().parent()
        val = parseInt(@points.val())
        min = parseInt(@points.attr('min'))
        max = parseInt(@points.attr('max'))
        pointsContainer.removeClass('error')
        $('.errorMsgPoints').remove()
        if not (min <= val and val <= max)
            pointsContainer.addClass('error')
            $('<span class="help-inline errorMsgPoints">Out of valid range.' +
                '</span>').insertAfter(@points)
            return null
        return val

    # Validates and returns the slot input number
    getSlots: ->
        slotsContainer = @slots.parent().parent()
        val = parseInt(@slots.val())
        min = parseInt(@slots.attr('min'))
        max = parseInt(@slots.attr('max'))
        slotsContainer.removeClass('error')
        $('.errorMsgPSlots').remove()
        if not (min <= val and val <= max)
            slotsContainer.addClass('error')
            $('<span class="help-inline errorMsgPSlots">Out of valid range.' +
                '</span>').insertAfter(@slots)
            return null
        else if (val > @candidateIDs.length and @getWriteInSlots() < 1)
            slotsContainer.addClass('error')
            $('<span class="help-inline errorMsgPSlots">Number of ' +
                'slots exceed number of candidates.</span>').insertAfter(@slots)
            return null
        return val

    # Resets the HTML form
    reset: ->
        super()
        @slots.val('1').change()

        # Remove errors
        pointsContainer = @points.parent().parent()
        pointsContainer.removeClass('error')
        $('.errorMsgPoints').remove()

        slotsContainer = @slots.parent().parent()
        slotsContainer.removeClass('error')
        $('.errorMsgPSlots').remove()

    # Gives the contents of the form in json form if valid, otherwise null
    toJson: =>
        position = super()
        return null if position == null
        json =
            'type': 'Cumulative-Voting'
            'slots': @getSlots()
            'points': @getPoints()
        for key, value of json
            return null if value == null
            position[key] = value
        return position

    setFromJson: (json) =>
        super(json)
        @points.val(json['points'])
        @slots.val(json['slots'])
