/**
 * JS for create.html
 */

// Contains the positions added in the election where each position is a literal object
var debug = false;
var positions = [];

/**
 * Initializes JS plug-ins and event listeners on the page.
 */
$(document).ready(function() {
	// Initialize the date / time pickers.
	$('#startDate').parent().datepicker();
	$('#startTime').timepicker({
		minuteStep : 5,
	});
	$('#endDate').parent().datepicker();
	$('#endTime').timepicker({
		minuteStep : 5,
	});

	// Form validation
	$('#election-submit').click(submitForm);
	$('#createForm').bind('reset', function() {
		currentModal.resetForm();
		positions = [];
		$('#positions-list').children().remove();
	});

	$('label[rel="tooltip"]').tooltip();

});

/**
 * Called when the submit button is clicked. Validates and makes an AJAX submission if form is valid.
 */
function submitForm() {
    if ($('#election-submit').hasClass('disabled')) {
        return false;
    }

	var valid = true;
	var formData = [getElectionName(), getElectionTimes(), getEligibleVoters(), getPositions()];
	$.each(formData, function(index, value) {
		if (value == null) {
			valid = false;
		}
	});

	var postData = {
	    'name': formData[0],
	    'start': formData[1]['start'],
	    'end': formData[1]['end'],
	    'voters': formData[2],
	    'positions': formData[3]
	};

	console.log(postData);
	if (valid) {
	    if (!debug) {
	       $('#election-submit').addClass('disabled');
	    }
		$.ajax({
		    url: '/createElection',
		    type: 'POST',
		    data: {'formData': JSON.stringify(postData)},
		    success: function(data) {
		        var response = JSON.parse(data);
		        $('html, body').animate({
                    scrollTop : $('#server-response').offset().top
                }, 500);
                $('#server-response').addClass('alert');
                if (response['status'] == 'OK') {
                    $('#server-response').addClass('alert-success');
                } else {
                    $('#server-response').addClass('alert-error');
                }
                $('#server-response').html(response['msg']);
                $('#server-response').hide().slideDown(1000);
		    },
		});
	} else {
		// Animate to name
		$('html, body').animate({
			scrollTop : $('#createForm').offset().top
		}, 500);
		return false;
	}
}

/**
 * Returns the election name.
 * @return {String} election name, null if input is invalid.
 */
function getElectionName() {
	var name = $('#name');
	var nameContainer = name.parent().parent();
	if (name.val() == '') {// Name not specified
		// Mark error if not already marked
		if (!nameContainer.hasClass('error')) {
			nameContainer.addClass('error');

			$('<span class="help-inline errorMsgName">Please enter election name.</span>').insertAfter(name);
		}
		return null;
	}

	// Valid election name
	if (nameContainer.hasClass('error')) {// Remove error mark
		nameContainer.removeClass('error');
		$('.errorMsgName').remove();
	}
	return name.val();

}

/**
 * Returns the start and end times in time since epoch.
 * @return {Object} start and end times keyed by 'start' and 'end'. null if input is invalid.
 */
function getElectionTimes() {
	var startDate = $('#startDate');
	var startTime = $('#startTime');
	var endDate = $('#endDate');
	var endTime = $('#endTime');
	var timeContainer = startDate.parent().parent().parent();
	var errorMessage = '';
	var start;
	// Return val
	var end;
	// Return val

	// Make sure user has entered all information
	if (!startDate.val() || !startTime.val() || !endDate.val() || !endTime.val()) {
		errorMessage = 'Missing information.';
	}

	if (!errorMessage) {
		// Validate start and end date / time
		var start = new Date(startDate.val() + ' ' + startTime.val()).getTime();
		var end = new Date(endDate.val() + ' ' + endTime.val()).getTime();
		start /= 1000;
		end /= 1000;
		console.log(start);
		console.log(end);
		if (start > end) {
			errorMessage = 'Start time is later than end time.';
		}
		if (start == end) {
			errorMessage = 'Start time is the same as end time.';
		}
	}

	if (errorMessage) {
		// Mark error if not already marked
		if (!timeContainer.hasClass('error')) {
			timeContainer.addClass('error');
		}

		// Clear existing error message
		$('.errorMsgTime').remove();

		// Add new error message
		startDate.parent().parent().append('<span class="help-inline errorMsgTime">' + errorMessage + '</span>');
		return null;
	} else {
		timeContainer.removeClass('error');
		$('.errorMsgTime').remove();
		return {
			'start' : start,
			'end' : end
		};
	}
}

/**
 * Returns the list of eligible voters the user has entered.
 * @return {Object} list of voters, null if input is invalid.
 */
function getEligibleVoters() {
	var voters = $('#eligible-voters');
	var votersContainer = voters.parent().parent();
	var errorMessage = '';
	var votersList = [];
	// Return val
	$.each(voters.val().split(','), function(index, value) {
		var voter = value.trim();
		if (voter) {
			votersList.push(voter);
		}
	});

	if (votersList.length == 0) {// Name not specified
		errorMessage = 'Missing information.';
	}

	// Remove existing errors
	votersContainer.removeClass('error');
	$('.errorMsgEligibleVoters').remove();
	console.log(errorMessage);
	if (errorMessage) {
		votersContainer.addClass('error');
		$('<span class="help-inline errorMsgEligibleVoters">' + errorMessage + '</span>').insertAfter(voters);
		return null;
	}
	return votersList;
}

/**
 * Returns the list of positions the user has entered.
 * @return {Object} list of position objects, null if there are no positions
 */
function getPositions() {
    if (debug) {
        return [];
    }
	var pos = $('#positions-list');
	var posContainer = pos.parent().parent();

	// Remove existing errors
	posContainer.removeClass('error');
	$('.errorMsgPositions').remove();
	if (positions.length == 0) {
		posContainer.addClass('error');
		$('<span class="help-inline errorMsgPositions">Need atleast one position.</span>').insertAfter(pos);
		return null;
	}
	return positions;
}

/**
 * Displays the specified position on the main page.
 * @param {Object} position a valid position
 */
function displayPosition(position) {
    var html = '<div style="margin: 5px 0 5px;"><strong>' + position['type'] + ': </strong>' + position['name'] +
            '<br /><ul>';
    $.each(position['candidates'], function(index, value) {
        html += '<li>' + value['name'] + ' - ' + value['netId'] + '</li>';
    });
    if (position['writeIn']) {
        html += '<li><em>Write-in</em></li>';
    }
    html += '</ul>';
    var newPos = $(html);
    $('#positions-list').append(newPos);
    newPos.hide().slideDown(1000);
}

function createSuccessResponse(data, status) {
    alert('\n\nresponseText: \n' + responseText + '\nstatus: ' + statusText);

    console.log('Form Reset');
    resetPositionForm();
    positions = [];
    $('#positions-list').children().remove();
}

/**
 * Add Position Modal Pop-up
 */
var addPositionModal = function() {
    var modal = this;                                             // Out of scope reference
    var candidatesIDs = [];                                       // List of HTML IDs of candidates added to the form
    var candidateIDGen = 0;                                       // Generator for candidate IDs
    var candidateIDPrefix = 'position-candidate-';                // HTML ID prefix for candidates
    var positionSelectType = $('#position-select-type');          // Drop-down: Position type
    var positionSelectionContent = $('.selection-content');       // Divs: Content for selected position types
    var rankedChoice = $('#ranked-choice');                       // Select: ranked choice position type
    var singleChoice = $('#single-choice');                       // Select: single choice position type
    var positionName = $('#position-name');                       // Text Input: Position name input
    var positionSlots = $('#position-slots');                     // Number Input: Position slots
    var positionAddCandidate = $('#position-add-candidate');      // Button: Add candidate
    var positionCandidates = $('#position-candidates');           // Div: list of candidates
    var positionWriteIn = $('#position-write-in');                // Checkbox: whether the position has a write-in
    var positionAddSubmit = $('#position-add-submit');            // Button: Add position

    /**
     * Resets the HTML form in the modal box on the page.
     */
    this.resetForm = function() {
        console.log('Reset Form');
        positionSelectType.val('0').change();
        candidatesIDs = [];
        positionCandidates.children().remove();
        positionSlots.val('1').change();
        positionName.val('').change();
        positionWriteIn.attr('checked', false);
    };

    /**
     * Updates the form when the position type is changed from the drop-down.
     */
    positionSelectType.change(function() {
        positionSelectionContent.hide();    // Hide all of the other selection content
        var selectedId = $(this).val();
        $('#' + selectedId).show();
    });

    /**
     * Adds an input field for a candidate to the form when add candidate button is clicked.
     */
    positionAddCandidate.click(function() {
        var index = candidateIDGen++;
        var id = candidateIDPrefix + index;

        var candidateInput = $('<div/>', {
            class : 'input-append'
        }).append($('<input>', {
            type : 'text',
            class : 'input-xlarge, input-margin-right',
            id : id + '-name',
            name : id + '-name',
            width : '200px',
            placeholder : "Full Name"
        })).append($('<input>', {
            type : 'text',
            class : 'input-xlarge',
            id : id + '-net-id',
            width : '50px',
            name : id + '-net-id',
            placeholder : "NetID"
        })).append($('<span/>', {
            class : 'add-on',
            id : id
        }).append($('<i/>', {
            class : 'icon-remove'
        })));
        $('#position-candidates').append(candidateInput);

        candidateInput.hide().fadeIn(500);
        candidatesIDs.push(index);

        // Delete candidate button
        $('#' + id).click(function() {
            var indexPtr = candidatesIDs.indexOf(index);
            if (indexPtr != -1) {
                candidatesIDs.splice(indexPtr, 1);
            }
            $(this).parent().fadeOut(500);
        });
    });

    /**
     * Returns the position type selected.
     */
    var getPositionType = function() {
        if (rankedChoice.attr('selected') == 'selected') {
            return 'Ranked-Choice';
        } else if (singleChoice.attr('selected') == 'selected') {
            return 'Single-Choice';
        }
    }

    /**
     * Validates and returns the position name typed.
     * TODO: Trim input
     */
    var getPositionName = function() {
        var positionNameContainer = positionName.parent().parent();
        // Remove existing errors
        positionNameContainer.removeClass('error');
        $('.errorMsgPositionName').remove();
        if (positionName.val() == '') {
            positionNameContainer.addClass('error');
            $('<span class="help-inline errorMsgPositionName">Missing information.</span>').insertAfter(positionName);
            return null;
        }
        return positionName.val();
    }

    /**
     * Validates and returns the slot input number.
     */
    var getSlots = function() {
        var slotsContainer = positionSlots.parent().parent();
        var slotsVal = parseInt(positionSlots.val());
        var slotsMin = parseInt(positionSlots.attr('min'));
        var slotsMax = parseInt(positionSlots.attr('max'));
        // Remove existing errors
        slotsContainer.removeClass('error');
        $('.errorMsgSlots').remove();
        if (!(slotsMin <= slotsVal && slotsVal <= slotsMax)) {
            slotsContainer.addClass('error');
            $('<span class="help-inline errorMsgSlots">Out of valid range.</span>').insertAfter(positionSlots)
            return null;
        } else if (slotsVal > candidatesIDs.length && !hasWriteIn()) {
            slotsContainer.addClass('error');
            $('<span class="help-inline errorMsgSlots">Number of ' +
                        'slots exceed number of candidates.</span>').insertAfter(positionSlots);
            return null;
        }
        return slotsVal;
    }

    /**
     * Validates and returns a list of candidates that the user has input.
     * Where each candidate is an object literal with keys name and netId.
     * TODO: Trim input
     */
    var getCandidates = function() {
        var missingInformation = false;
        var candidatesContainer = positionCandidates.parent().parent();
        var candidates = [];        // Function output

        // Make sure the candidate name is defined for all candidates
        $.each(candidatesIDs, function(index, value) {
            var candidateNameInput = $('#position-candidate-' + value + '-name');
            var candidateNetIDInput = $('#position-candidate-' + value + '-net-id');
            if (candidateNameInput.val() == '' || candidateNetIDInput.val() == '') {
                missingInformation = true;
            } else {
                candidates.push({'name': candidateNameInput.val(),
                                 'netId': candidateNetIDInput.val()});
            }
        });

        // Remove existing errors
        $('.errorMsgCandidateName').remove();
        candidatesContainer.removeClass('error');
        if (missingInformation) {
            candidatesContainer.addClass('error');
            $('<span class="help-inline errorMsgCandidateName">' +
                    'Missing information.</span>').insertAfter(positionCandidates);
            return null;
        }

        return candidates;
    }

    /**
     * Returns whether the user specified a write-in for this position.
     */
    var hasWriteIn = function() {
        if (positionWriteIn.attr('checked') == 'checked') {
            return true;
        }
        return false;
    }

    /**
     * Validates all position form entries and adds to the main election form.
     */
    positionAddSubmit.click(function() {
        var valid = true;
        var formData = [getPositionType(), getPositionName(), getSlots(), getCandidates(), hasWriteIn()];
        $.each(formData, function(index, value) {
            if (value == null) {
                valid = false;
            }
        });
        if (valid) {
            var position = {
                'type' : formData[0],
                'name' : formData[1],
                'slots' : formData[2],
                'candidates' : formData[3],
                'writeIn': formData[4]
            };
            positions.push(position);
            displayPosition(position);
            $('#addPositions').modal('hide');
            modal.resetForm();
        }
    });
};

var currentModal = new addPositionModal();
