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
    $('#election-submit').addClass('disabled');

    /* Get the ballot before validating it, not the other way around. */
	var ballot = getBallot();
    console.log(ballot);

    /* Don't submit a ballot that does not validate. */
    if (! ballotValidates(ballot)) {
        $('#election-submit').removeClass('disabled');
        return false;
    }

    console.log("It validated. TODO!")
    return false; // todo

    $.ajax({
        url: '/submit-ballot',
        type: 'POST',
        data: {'formData': JSON.stringify(ballot)},
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
}

/**
 *
 *@returns {Ballot} Returns a ballot object built from the user's input.
 */
function getBallot() {

    var ballot = {}

    /* For each position, get the position and the data. */
    $('.position').each(function(i, obj) {

        var name = $(this).attr('data-name')
        var type = $(this).attr('data-type')
        var id   = $(this).attr('data-id')

        /* Ranked Choice info gathering. */
        if (type == 'Ranked-Choice') {
            ballot[name] = {};
            ballot[name]['front_end_id'] = id;
            ballot[name]['candidates'] = {}
            ballot[name]['candidate_count'] = 0

            /* Get the data from each of the children running for office. */
            $('.'+id).each(function(i, obj) {

                var candidate_name = $(this).attr('data-candidate-name')
                var candidate_rank = parseInt($(this).val())

                /* Get the real name if this is a write-in candidate. */
                if (candidate_name == 'write-in') {
                    candidate_name = $('#write-in-name').val()
                }

                /* Ignore blank write-ins. */
                if (candidate_name != '') {
                    ballot[name]['candidates'][candidate_name] = candidate_rank
                    ballot[name]['candidate_count']++;
                }
            });

        } else {
            // TODO: non-ranked elections
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

    $.each(ballot, function(name, choices) {
        var id = ballot[name]['front_end_id']
        var candidates = ballot[name]['candidates']
        var candidate_count = ballot[name]['candidate_count'];

        /* We want to check for the ranks 1-(candidates.length+1). */
        var rank_check = []
        for (var i = 0; i < candidate_count; i++) {
            rank_check[i] = false;
        }

        /* For each candidate, check their rank. */
        $.each(candidates, function(name, rank) {

            /* Do not accept empty ranks or non number ranks. */
            if (!$.isNumeric(rank)) {
                valid = false;
                $('#' + id + '-error').addClass('text-error');
            }

            /* Keep track of which ranks we have seen. */
            rank_check[rank-1] = true;
        });

        /* If any rank was missing, the person tied at least two candidates. */
        for (var i = 0; i < rank_check.length; i++) {
            if (rank_check[i] != true) {
                valid = false;
                $('#' + id + '-error').addClass('text-error');
            }
        }

    });

    return valid;
}