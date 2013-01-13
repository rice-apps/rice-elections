/**
 * JS for cast-ballot.html
 */

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

    /* Get the ballot before validating it, not the other way around. */
	var ballot = getBallot();
    console.log(ballot);

    /* Don't submit a ballot that does not validate, but let a user fix it. */
    if (! ballotValidates(ballot)) {
        $('#cast-ballot-button').removeClass('disabled');
        return false;
    }

    $.ajax({
        url: '/submit-ballot',
        type: 'POST',
        data: {'formData': JSON.stringify(ballot)},
        success: function(data) {
            var response = JSON.parse(data);
            // TODO: make better / more modular error / success handlers
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
        error: function(data) {
            // TODO: make better / more modular error / success handlers
            $('html, body').animate({
                scrollTop : $('#server-response').offset().top
            }, 500);
            $('#server-response').addClass('alert');
            $('#server-response').addClass('alert-error');
            $('#server-response').html("An error occurred when your data was submitted. Please refresh the page and try to vote again. If that doesn't fix your problem, please <a href='/contact'> contact us</a>.");
            $('#server-response').hide().slideDown(1000);
        }
    });
}

/**
 *
 *@returns {Ballot} Returns a ballot object built from the user's input.
 */
function getBallot() {

    var ballot = {}
    ballot['positions'] = []

    /* For each position, get the position and the data. */
    $('.position').each(function(i, obj) {

        var name = $(this).attr('data-name')
        var type = $(this).attr('data-type')
        var id   = $(this).attr('data-id')

        /* Ranked Choice info gathering. */
        if (type == 'Ranked-Choice') {
            var position = {};
            position['id'] = id;
            position['name'] = name;
            position['type'] = type;
            position['candidate_rankings'] = []

            /* Get the data from each of the children running for office. */
            $('.'+id).each(function(i, obj) {

                var candidate_id   = $(this).attr('data-candidate-id')
                var candidate_name = $(this).attr('data-candidate-name')
                var candidate_rank = $(this).val() ? parseInt($(this).val()) : ''

                /* Get the real name if this is a write-in candidate. */
                if (candidate_name == 'write-in') {
                    candidate_name = $('#write-in-name').val()
                }

                /* Ignore blank write-ins. */
                if (candidate_name != '') {
                    var candidate = {
                        'name' : candidate_name,
                        'id'   : candidate_id,
                        'rank' : candidate_rank
                    }
                    position['candidate_rankings'].push(candidate)
                }
            });

            ballot['positions'].push(position)

        } else {
            // TODO: non-ranked elections
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
    $('.error-texts').removeClass('text-error')
    var valid = true;

    /* Check each position to see if the candidates were ranked correctly. */
    $.each(ballot['positions'], function(i, position) {
        var id         = position['id']
        var candidates = position['candidate_rankings']
        var candidate_count = candidates.length;

        /* We want to check for the ranks 1-(candidates.length+1). Either they
         * must all be ranked or none of them must be ranked. */
        var rank_check = [];
        position['skipped'] = true;
        for (var i = 0; i < candidate_count; i++) {
            rank_check[i] = false;
            if (candidates[i]['rank'] != '') {
                position['skipped'] = false;
            }
        }

        if (! position['skipped']) {
            /* For each candidate, check their rank. */
            $.each(candidates, function(i, candidate) {

                var rank = candidate['rank'];

                /* Do not accept empty ranks or non number ranks. */
                if (!$.isNumeric(rank)) {
                    valid = false;
                    $('#' + id + '-error').addClass('text-error');
                }

                rank_check[rank-1] = true;
            });

            /* Ensure all ranks were used exactly once. */
            for (var i = 0; i < rank_check.length; i++) {
                if (rank_check[i] != true) {
                    valid = false;
                    $('#' + id + '-error').addClass('text-error');
                }
            }
        }

    });

    return valid;
}