__author__ = 'Savion Lee'

# The purpose of the new results report is to increase readability for the
# organization admin.

import logging
import models
import webapp2

from google.appengine.ext import db
from google.appengine.api import mail
from algorithms_ import irv, cv
from jinja2 import Template
from datetime import datetime


def gather_ballots(pos):
    """
    Returns a list of ballots for the position passed in.
    :param pos: position Object
    :return: list of ballots
    """
    ballots_db = pos.ballots.fetch(100)
    ballots = []
    while ballots_db:
        for ballot in ballots_db:
            can_names = [db.get(can).name for can in ballot.preferences]
            ballots.append(can_names)

        ballots_db = pos.ballots.filter('__key__ >', ballots_db[-1].key()).fetch(100)

    return ballots



def email_election_results(to, election):
    """
    Sends an email to the election admin with the results.

    :param to: <List (admin_emails)>
    :param election: Election Object
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

    email_message = Template(source='../views/email_report.html')
    message.body = email_message.render(positions=positions)
    message.send()
