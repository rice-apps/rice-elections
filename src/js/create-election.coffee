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
	getElectionName()
	getElectionTimes()
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

getPositions = ->
	pos = $('#positions-list')
	posContainer = pos.parent().parent()
	posContainer.removeClass('error')
	$('.errorMsgPositions').remove()
	if not all_positions
		posContainer.addClass('error')
		$("<span class='help-inline errorMsgPositions'>Need at least one " +
			"position.</span>").insertAfter(pos);
		return null
	return all_positions

displayPosition = (position) ->
	html = "<div style='margin: 5px 0 5px;'><strong>#{position['type']}: " +
			"</strong>#{position['name']}<br /><ul>"
	for candidate in position['candidates']
		html += "<li>#{candidate['name']} = #{candidate['netId']}</li>"
	if position['vote_required']
		html += "<li><em>Vote required</em></li>"
	html += "</ul>"
	newPos = $(html)
	$('#positions-list').append(newPos)
	newPos.hide().slideDown(1000)

class positionModal
	candidateIDs = []	 # List of HTML IDs of candidates added to the form
	candidateIDGen = 0	 # Generator for candidate IDs
	candidateIDPrefix = 'position-candidate-'  # HTML ID prefix for candidates
	selectType = $('#position-select-type')    # Drop-down: Position type
	selectionContent = $('.selection-content') # Divs: selected position types
	rankedChoice = $('#ranked-choice')    # Select: ranked choice position type
	cumulativeVoting = $('#cumulative-voting') # Select: cumulative voting pos
	name = $('#position-name')		# Text Input: Position name input
	slots = $('#position-slots')	# Number Input: Position slots
	addCandidate = $('#position-add-candidate')	  # Button: Add candidate
	candidates = $('#position-candidates')		  # Div: list of candidates
	writeIn = $('#position-write-in') 
	voteRequired = $('#position-required')		 # Checkbox
	addSubmit = $('#position-add-submit')		 # Button
	
	resetForm: ->		  # Resets the HTML form in the modal box on the page.
		selectType.val('0').change()
		candidateIDs = []
		candidates.children().remove()
		slots.val('1').change()
		name.val('').change()
		writeIn.attr('checked', false)
		voteRequired.attr('checked', false)
	
	selectType.change ->   # Updates the form when the position type is changed
		selectionContent.hide()
		$("##{$(this).val()}").show()
	
	addCandidate.click ->	# Adds an input field for a candidate to the form
		index = candidateIDGen++
		id = candidateIDPrefix + index
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
			id: id
		).append($('<i/>',
			class: 'icon-remove'
		)))
		candidates.append(candidateInput)
		candidateInput.hide().fadeIn(500)
		candidateIDs.push(index)
		
		# Delete candidate button
		$("##{id}").click ->
			indexPtr = candidateIDs.indexOf(index)
			candidateIDs.splice(indexPtr, 1) if indexPtr != -1
			$(this).parent().fadeOut(500)
		
	getType = ->	# Returns the position type selected.
		if rankedChoice.attr('selected') == 'selected'
			return 'Ranked-Choice' 
		if rankedChoice.attr('selected') == 'selected'
			return 'Cumulative-Voting' 
	
	getName = ->	# Validates and returns the position name typed.
		nameContainer = name.parent().parent()
		nameContainer.removeClass('error')
		$('.errorMsgPositionName').remove()
		if not name.val()
			nameContainer.addClass('error')
			$('<span class="help-inline errorMsgPositionName">Missing ' +
				'information.</span>').insertAfter(name)
			return null
		return name.val()
	
	getSlots = ->	 # Validates and returns the slot input number.
		slotsContainer = slots.parent().parent()
		val = parseInt(slots.val())
		min = parseInt(slots.attr('min'))
		max = parseInt(slots.attr('max'))
		slotsContainer.removeClass('error')
		$('.errorMsgSlots').remove()
		if not (min <= val and val <= max)
			slotsContainer.addClass('error')
			$('<span class="help-inline errorMsgSlots">Out of valid range.' +
				'</span>').insertAfter(slots)
			return null
		else if (val > candidateIDs.length and not hasWriteIn())
			slotsContainer.addClass('error')
			$('<span class="help-inline errorMsgSlots">Number of ' +
				'slots exceed number of candidates.</span>').insertAfter(slots)
			return null
		return val
	
	getCandidates = ->		# Validates and returns a list of candidates
		missing = false
		container = candidates.parent().parent()
		canList = []	# Function output
		
		# Make sure the candidate name is defined for all candidates
		for can in candidateIDs
			nameInput = $("#position-candidate-#{can}-name")
			netIdInput = $("#position-candidate-#{can}-net-id")
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
				'Missing information.</span>').insertAfter(candidates)
			return null
		
		return canList
	
	hasWriteIn = -> true if writeIn.attr('checked') == 'checked'
	
	hasVoteRequirement = -> true if voteRequired.attr('checked') == 'checked'
	
	addSubmit.click (e) =>
		console.log('Submit clicked')
		position =
			'type': getType()
			'name': getName()
			'slots': getSlots()
			'candidates': getCandidates()
			'write_in': hasWriteIn()
			'vote_required': hasVoteRequirement()
		for key, value of position
			return false if value == null
		all_positions.push(position)
		displayPosition(position)
		$('#addPositions').modal('hide')
		currentModal.resetForm()
		# TODO: Find a way to reference self, this.resetForm() doesn't work nor
		# does modalPosition.resetForm() 
	
currentModal = new positionModal()



