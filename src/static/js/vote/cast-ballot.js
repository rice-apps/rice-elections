/**
 * JS for cast-ballot.html
 */

var valid;
var reasonsInvalid;

/**
 * Initializes JS event listeners on the page.
 */
$(document).ready(function() {

    /* Submit the ballot when the user clicks the cast ballot button. */
    $('#cast-ballot-button').click(function(){
        submitForm();
        return false;
    });
});

/**
 * Called when the submit button is clicked. Validates and makes an AJAX
 * submission if form is valid.
 */
function submitForm() {

    /* Don't resubmit a form. */
    if ($('#cast-ballot-button').hasClass('disabled')) {
        return false;
    }

    /* Immediately disable the button. */
    $('#cast-ballot-button').addClass('disabled');
    hideResult();

    /* Get the ballot before validating it, not the other way around. */
	var ballot = getBallot();
    console.log(ballot);

    /* Don't submit a ballot that does not validate, but let a user fix it.
     * Give them a pop up with a list of things they need to fix. */
    if (! ballotValidates(ballot)) {
        $('#cast-ballot-button').removeClass('disabled');

        /* The boilerplate message. */
        var message = $('<div>', {
            text : 'There seems to be a problem with your ballot. Please try fixing it and submitting again!'
        });

        /* The list of reasons their ballot is invalid. */
        var list = $('<ul>');
        $.each(reasonsInvalid, function(i, reason) {
            list.append($('<li>', {
                text: reason
            }));
        });

        message.append(list);
        showResult(false, message);

        return false;
    }

    /* Testing code for front-end validation. */
    // console.log("Testing mode on.");
    // $('#cast-ballot-button').removeClass('disabled');
    // return false;

    /* Send the ballot off and handle a response from the server. */
    $.ajax({
        url: '/vote/cast-ballot',
        type: 'POST',
        data: {'formData': JSON.stringify(ballot)},
        success: function(data) {
            var response = JSON.parse(data);
            var success = (response['status'] == 'OK') ? true : false;
            showResult(success, response['msg']);
        },
        error: function(data) {
            showResult(false, "An error occurred when your data was submitted. Please refresh the page and try to vote again. If that doesn't fix your problem, please <a href='/contact'> contact us</a>.");
        }
    });
}

// TODO: make this function to be more extensible once the initial set of elections are over.
/**
 * Returns a ballot object built from the user's input.
 */
function getBallot() {

    var ballot = {}
    ballot['election_id'] = $('#election-information').attr('data-election-id');
    ballot['positions'] = [];

    /* For each position, get the position and the data. */
    $('.position').each(function(i, obj) {

        var write_in = false;
        var name     = $(this).attr('data-name');
        var type     = $(this).attr('data-type');
        var id       = $(this).attr('data-id');
        var required = ($(this).attr('data-vote-required') == 'True') ? true : false;
        var available_points = $(this).attr('data-available-votes');

        /* Ranked Choice and cumulative info gathering. */
        if (type == 'Ranked-Choice' || type == 'Cumulative-Voting') {
            var position = {};
            position['id'] = id;
            position['name'] = name;
            position['type'] = type;
            position['required'] = required;

            /* Initialize the containers for the votes and other type specific
            *  information . */
            if (type == 'Ranked-Choice') {
                position['candidate_rankings'] = [];
            }else if (type == 'Cumulative-Voting') {
                position['candidate_points'] = [];
                position['available_points'] = available_points;
            }

            /* Get the data from each of the children running for office. */
            $('.'+id).each(function(i, obj) {

                var candidate_id   = $(this).attr('data-candidate-id')
                var candidate_name = $(this).attr('data-candidate-name')

                /* Get the real name if this is a write-in candidate. */
                if (candidate_name == 'write-in') {
                    candidate_name = $("#" + candidate_id + "-name").val();
                    write_in = true;
                }

                /* If the candidate name is empty or their is a input. */
                if (candidate_name != '' || $(this).val()) {
                    if (type == 'Ranked-Choice') {
                        var candidate_rank = ($(this).val() && isInt($(this).val())) ? parseInt($(this).val()) : $(this).val()
                        var candidate = {
                            'name' : candidate_name,
                            'id'   : candidate_id,
                            'rank' : candidate_rank,
                            'write_in' : write_in
                        }
                        position['candidate_rankings'].push(candidate)
                    }
                    if (type == 'Cumulative-Voting') {
                        var candidate_points = ($(this).val() && isInt($(this).val())) ? parseInt($(this).val()) : 0
                        var candidate = {
                            'name' : candidate_name,
                            'id'   : candidate_id,
                            'points' : candidate_points,
                            'write_in' : write_in
                        }
                        position['candidate_points'].push(candidate);
                    }
                }
            });

            ballot['positions'].push(position)

        } else {
            // TODO: non-ranked / non-cumulative elections, Basically Radio Button
            console.log("This has yet to be implemented yet.")
        }
    });

    return ballot
}

/**
 *
 * @returns {Boolean} true if the user input validates, false otherwise.
 */
function ballotValidates(ballot) {

    /* Assume it is all valid until proven otherwise. */
    $('.error-texts').removeClass('text-error');
    valid = true;
    reasonsInvalid = [];

    /* Check each position to see if it validates. */
    $.each(ballot['positions'], function(i, position) {
        var type  = position['type'];
        if (type == 'Ranked-Choice') {
            verifyRankedPosition(position);
        } else if (type == 'Cumulative-Voting') {
            verifyCummulativePosition(position);
        }
    });

    // TODO Verify radio ballot

    return valid;
}

/**
 * Function that verifies a cummulative position is valid.
 */
function verifyCummulativePosition(position) {
    var id    = position['id']
    var name  = position['name']
    var type  = position['type']
    var candidates = position['candidate_points']
    var available_points = position['available_points'];
    var write_in = false;
    var sum = 0;

    $.each(candidates, function(i, candidate) {
        var votes = candidate['points'];
        var write_in = candidate['write_in'];
        var candidate_name = candidate['name'];

        /* Verify all write-ins have a name. */
        if (write_in && candidate_name == '' && votes != 0)
            invalidate(id, name, 'A write-in with votes must have a name.');

        /* Verify all write-ins have a vote. */
        if (write_in && candidate_name != '' && votes == 0)
            invalidate(id, name, 'A non-empty write-in must have votes.');

        /* Verify that votes are non negative integers. */
        if (!$.isNumeric(votes) || votes < 0 || !isInt(votes)) {
            invalidate(id, name, 'Number of votes cast must be a non-negative integer.');
        }else {
            sum += votes;
        }

    });

    /* Any non-zero number of votes not equal to sum is invalid.*/
    if (sum != available_points && sum != 0)
        invalidate(id, name, 'The sum of your points must be ' + available_points + '.');

    /* If the position requires a vote and it was skipped, error. */
    if(sum == 0 && position['required'])
        invalidate(id, name, 'Your vote for this position is required.');
}

function verifyRankedPosition(position) {
    var id    = position['id']
    var name  = position['name']
    var type  = position['type']
    var write_in = false;
    var candidates = position['candidate_rankings']
    var candidate_count = candidates.length;

    /* We want to check for the ranks 1-(candidates.length+1). Either
     * they must all be ranked or none of them must be ranked. */
    var rank_check = [];
    position['skipped'] = true;
    for (var i = 0; i < candidate_count; i++) {
        rank_check[i] = false;
        if (candidates[i]['rank'] != '') {
            position['skipped'] = false;
        }
        if (candidates[i]['write_in']) {
            position['skipped'] = false;
        }
    }

    /* If the position requires a vote and the user skipped it, error. */
    if (position['skipped'] && position['required'])
        invalidate(id, name, 'Your vote for this position is required.');

    /* Make sure ranks are unique and complete. */
    if (!position['skipped']) {
        $.each(candidates, function(i, candidate) {
            var rank = candidate['rank'];
            var write_in = candidate['write_in'];
            var candidate_name = candidate['name'];

            /* The rank must be an integer. */
            if (!$.isNumeric(rank) || !isInt(rank))
                invalidate(id, name, 'All candidates must be ranked with a integer rank in the range from 1 to ' + candidate_count + '.');

            /* Verify all write-ins have a rank. */
            if (write_in && candidate_name == '' && rank != '')
                invalidate(id, name, 'A ranked write-in must have a name.');

            /* Verify all ranked write-ins have a name. */
            if (write_in && candidate_name != '' && rank == '')
                invalidate(id, name, 'A write-in must be ranked.');

            rank_check[rank-1] = true;
        });

        /* Ensure all ranks were used exactly once. */
        for (var i = 0; i < rank_check.length; i++) {
            if (rank_check[i] != true) {
                invalidate(id, name, 'All candidates must be ranked with a integer rank in the range from 1 to ' + candidate_count + '.');
            }
        }
    }
}

/**
 * Invalidate the ballot for the reason given. Keep track of these reasons so
 * that the user might be told about them.
 */
function invalidate(id, name, message) {
    valid = false;
    $('#' + id + '-error').addClass('text-error');
    message = "["+name+"] " + message;
    if ($.inArray(message, reasonsInvalid) == -1)
        reasonsInvalid.push(message);
}

/**
 * Show the result of some action at the top of the ballot.
 */
function showResult(success, message) {
    $('#server-response').addClass('alert');
    $('#server-response').removeClass('alert-success');
    $('#server-response').removeClass('alert-error');
    if (success) {
        $('#server-response').addClass('alert-success');
    } else {
        $('#server-response').addClass('alert-error');
    }
    $('#server-response').html(message);
    $('#server-response').show(function() {
        $('html, body').animate({
            scrollTop : $('#server-response').offset().top - 20
        }, 500);
    });
}

function hideResult() {
    $('#server-response').hide();
}

function isInt(n) {
    return parseFloat(n) == parseInt(n);
}