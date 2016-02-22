__author__ = 'Savion Lee'

# The purpose of the new results report is to increase readability for the
# organization admin.

import logging
import models
import webapp2
from google.appengine.ext import db
from google.appengine.api import mail
from algorithms_ import irv, cv
from webapputils import JINJA_ENV
from datetime import datetime


def gather_ballots(pos):
    """
    Returns a list of ballots for the position passed in.
    :param pos: position Object
    :return: list of ballots
    """

    ballots = []
    if pos.position_type == 'Ranked-Choice':
        for ballot in pos.ballots:
            if pos.position_type == 'Ranked-Choice':
                can_names = [db.get(can).name for can in ballot.preferences]
                ballots.append(can_names)

    elif pos.position_type in ['Boolean-Voting', 'Cumulative-Voting']:
        for ballot in pos.ballots:
            ballot_dict = {}
            for choice in ballot.choices:
                candidate_name = choice.candidate.name
                ballot_dict[candidate_name] = choice.points
            ballots.append(ballot_dict)

    return ballots


def email_election_results(to, election, pos=None):
    """
    Sends an email to the election admin with the results.

    :param to: <List (admin_emails)>
    :param election: Election Object
    :param pos: Optional Position Object
    :return: none
    """

    message = mail.EmailMessage(
        sender="no-reply@owlection.appspotmail.com",
        reply_to="stl2@rice.edu",
        subject="Election Report for {elec_name}".format(elec_name=election.name)
    )
    message.to = ', '.join(to)

    positions = []
    # a position is a mapping of {'name': name, 'type': type, 'vote_required': vote_required,
    #                             'candidates': candidates, 'write-ins':write_ins, 'winner':winner,
    #                             'rounds': {{'number': 1, 'majority': majority?, 'remaining': remaining_candidates,
    #                                         'cut': cut_candidates}, ...}, 'points': points}

    positions_to_determine = []

    if pos:
        logging.info('[Report] Sending Position Report for {0} to {1}'.format(election.name, str(to)))
        positions_to_determine.append(pos)

    else:
        logging.info('[Report] Sending Election Report for {0} to {1}'.format(election.name, str(to)))
        # Gather Ranked Positions
        ranked_positions = models.RankedVotingPosition.gql("WHERE election=:1", election).fetch(None)
        positions_to_determine.extend(ranked_positions)

        # Gather Cumulative Positions
        cumulative_positions = models.CumulativeVotingPosition.gql("WHERE election=:1", election).fetch(None)
        positions_to_determine.extend(cumulative_positions)

        # Gather Boolean Positions
        boolean_positions = models.BooleanVotingPosition.gql("WHERE election=:1", election).fetch(None)
        positions_to_determine.extend(boolean_positions)

    for pos in positions_to_determine:
        new_position = {}
        json = pos.to_json()
        new_position.update(json)
        new_position['candidates'] = [can['name'] for can in json['candidates']]
        new_position['winners'] = [can['name'] for can in json['candidates'] if can['winner'] == True]

        if pos.position_type == 'Ranked-Choice':
            # Gather Ranked ballots
            ballots = gather_ballots(pos)
            computed_rounds = irv.run_the_rounds(ballots)
            new_position.update({'rounds': computed_rounds})

        if pos.position_type == ('Boolean-Voting' or 'Cumulative-Voting'):
            ballots = gather_ballots(pos)

            counts = cv.get_counts(ballots)

            new_position.update({'points': counts})

        positions.append(new_position)

    email_message = JINJA_ENV.get_template('email_report.html')
    logging.info('[Report] Rendering Email')
    message.html = email_message.render(positions=positions)
    message.send()
    logging.info('[Report] Email Sent!')
