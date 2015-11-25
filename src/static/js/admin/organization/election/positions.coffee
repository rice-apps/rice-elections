# JS for election panel positions.html

# Positions added in the election where each position is an object literal
all_positions = []
rankedModal = null
cumulativeModal = null
booleanModal = null
form = null
postUrl = '/admin/organization/election/positions'

jQuery ->
    rankedModal = new RankedVotingPosition()
    cumulativeModal = new CumulativeVotingPosition()
    booleanModal = new BooleanVotingPosition()
    form = new Form()

# Form for managing positions
class Form
    constructor: ->
        @positions = []

        # Reset modal each time add position is clicked
        $("a[href=#modal-ranked]").click =>
            rankedModal.reset()
        $("a[href=#modal-cumulative]").click =>
            cumulativeModal.reset()
        $("a[href=#modal-boolean]").click =>
            booleanModal.reset()

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
                    @createPositionHTML(position)
            error: (data) =>
                console.log('Unknown error')

    createPositionHTML: (position) =>
        html = $('<tr>',
            style: 'padding-bottom:5px;')
            .append($('<td>')
                .append($('<i>',
                    class: 'icon-user'))
                .append(" #{position['name']}"))
            .append($('<td>')
                .append($('<a>',
                    href: '#'
                    class: 'edit-position')
                    .append("Edit"))
                .append(" &middot; ")
                .append($('<a>',
                    href: '#'
                    class: 'delete-position')
                    .append("Delete")))

        console.log(html)
        $('#positions').append(html)
        $('#no-positions').hide()
        html.hide().slideDown(500)

        # Add event listener for edit position link
        html.children().children().filter('.edit-position').click =>
            data =
                'method': 'get_position'
                'id': position['id']
            $.ajax
                url: postUrl
                type: 'POST'
                data:
                    'data': JSON.stringify(data)
                success: (data) =>
                    response = JSON.parse(data)
                    position = response['position']
                    @editPosition(position)

        # Add event listener for delete position link
        html.children().children().filter('.delete-position').click =>
            $('.position-name').html(position['name'])
            $('#modal-confirmation').modal('show')
            $('#delete-position-yes').unbind("click")
            $('#delete-position-yes').click =>
                $('#modal-confirmation').modal('hide')
                data =
                    'method': 'delete_position'
                    'id': position['id']
                $.ajax
                    url: postUrl
                    type: 'POST'
                    data:
                        'data': JSON.stringify(data)
                    success: (data) =>
                        response = JSON.parse(data)
                        if response['status'] == 'OK'
                            html.slideUp(500)


    editPosition: (position) =>
        if position['type'] == 'Ranked-Choice'
            rankedModal.reset()
            rankedModal.setFromJson(position)
            $("#modal-ranked").modal('show')
        else if position['type'] == 'Cumulative-Voting'
            cumulativeModal.reset()
            cumulativeModal.setFromJson(position)
            $("#modal-cumulative").modal('show')
        else if position['type'] == 'Boolean-Voting'
            booleanModal.reset()
            booleanModal.setFromJson(position)
            $("#modal-boolean").modal('show')

# Abstract base class different position types, replace type in subclasses
class Position
    constructor: (@type) ->
        # Datastore entity ID
        @id = null

        # Position type
#        @type = type

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

        # Description (optional description for position)
        @description = $("#position-#{@type}-description") 
        
        # Bind events
        @submit.click(@submitData)
        @addCandidate.click(@addCandidateSlot)

    # Gives the contents of the form in json form if valid, otherwise null
    toJson: =>
        position =
            'id': @id
            'name': @getName()
            'candidates': @getCandidates()
            'write_in_slots': @getWriteInSlots()
            'vote_required': @hasVoteRequirement()
            'description': @getDescription()
        for key in ['name', 'candidates', 'write_in_slots', 'vote_required']
            return null if position[key] == null
        return position

    setFromJson: (json) =>
        return if not json
        @reset()
        @id = json['id']
        @writeInSlots.val(json['write_in_slots'])
        @voteRequired.prop('checked', json['vote_required'])
        @name.val(json['name'])
        @description.val(json['description'])
        for candidate in json['candidates']
            @addCandidateSlot()
            index = @candidateIDGen - 1
            id = @candidateIDPrefix + index
            $("##{id}-name").val(candidate['name'])
            $("##{id}-name").data('id', candidate['id'])
        @resetSubmitBtn()

    # Resets the HTML form
    reset: =>
        @candidateIDs = []
        @candidates.children().remove()
        @name.val('').change()
        @voteRequired.prop('checked', false)
        @id = null
        @resetSubmitBtn()
        @description.val("")

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

        method = 'add_position'
        if @id
            method = 'update_position'

        data =
            'method': method
            'position': position

        $.ajax
            url: postUrl
            type: 'POST'
            data:
                'data': JSON.stringify(data)
            success: (data) =>
                response = JSON.parse(data)
                if response['status'] == 'ERROR'
                    @setSubmitBtn('btn-danger', response['msg'])
                    console.log("Error: #{response['msg']}")
                    return
                if response['status'] == 'OK'
                    $("#modal-#{@type}").modal('hide')
                    @reset()
                    if method == 'add_position'
                        form.createPositionHTML(response['position'])
            error: (data) =>
                @setSubmitBtn('btn-danger', 'Error')

    # Resets the submit button ready for use
    resetSubmitBtn: =>
        text = 'Create Position'
        if @id
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
        
    # Gets the description for a position
    getDescription: ->
        return @description.val()
        
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
                canData = {'name': nameInput.val()}
                canId = nameInput.data('id')
                if canId
                    canData['id'] = canId
                canList.push(canData)

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
    hasVoteRequirement: -> @voteRequired.prop('checked')

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

class BooleanVotingPosition extends Position
    constructor: ->
        super('boolean')

        # Number Input: Position slots
        @slots = $('#position-cumulative-slots')

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

        slotsContainer = @slots.parent().parent()
        slotsContainer.removeClass('error')
        $('.errorMsgPSlots').remove()

    # Gives the contents of the form in json form if valid, otherwise null
    toJson: =>
        position = super()
        return null if position == null
        json =
            'type': 'Boolean-Voting'
            'slots': @getSlots()
        for key, value of json
            return null if value == null
            position[key] = value
        return position

    setFromJson: (json) =>
        super(json)
        @slots.val(json['slots'])

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
