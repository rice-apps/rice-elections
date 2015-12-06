"""
Script to report election results including ballots in detail to election admin.
"""

__author__ = 'Waseem Ahmad <waseem@rice.edu>'


import logging
import models
import webapp2

from google.appengine.ext import db
from google.appengine.api import mail
from datetime import datetime


def encode(string):
    try:
        return unicode(string, 'utf-8')
    except (TypeError, UnicodeDecodeError):
        return string

def email_pos_report(to, pos):
    """
    Sends an email to the election admin with the results and ballots 
    for a specific position.
    """
    election = pos.election
    message = mail.EmailMessage(
        sender="no-reply@owlection.appspotmail.com",
        subject="Election Report for %s: %s" % 
            (pos.election.name, pos.position.name))
    message.to = ', '.join(to)

    if pos.position_type == "Ranked-Choice":
        json = pos.to_json()
        string = u"""
Position Name: {0},
Vote Required: {1},
Write-in Slots: {2},
Candidates: {3},
Winners: {4}""".format(pos.position.name,
                       pos.vote_required,
                       pos.write_in_slots,
                       u', '.join([encode(can.name) for can in pos.election_position_candidates]),
                       u', '.join([encode(db.get(winner).name) for winner in pos.winners]))
    
        counts = {}
        ballots = []
        for ballot in pos.ballots:
            can_names = [db.get(can).name for can in ballot.preferences]
            ballots.append(u'[' + u','.join(can_names) + u']')
            if can_names:
                if can_names[0] in counts:
                    counts[can_names[0]] += 1
                else:
                    counts[can_names[0]] = 1
        string += u'\nBallots Cast:\n' + u'\n'.join(ballots) + u'\n'
        string += u'Total First Preference Counts: %s' % counts
    elif pos.position_type == "Cumulative-Voting":
        json = pos.to_json()
        string = u"""
Position Name: {0},
Vote Required: {1},
Write-in Slots: {2},
Position Slots: {3},
Points per voter: {4},
Candidates: {5},
Winners: {6}""".format(encode(pos.position.name),
                       pos.vote_required,
                       pos.write_in_slots,
                       pos.slots,
                       pos.points,
                       u', '.join([encode(can.name) for can in pos.election_position_candidates]),
                       u', '.join([encode(db.get(winner).name) for winner in pos.winners]))
        counts = {}
        ballots = []
        for ballot in pos.ballots:
            choices = []
            for choice in ballot.choices:
                choices.append(u'%s: %d' % (choice.candidate.name, choice.points))
                if choice.candidate.name in counts:
                    counts[choice.candidate.name] += choice.points
                else:
                    counts[choice.candidate.name] = choice.points
            ballots.append(u'{' + u', '.join(choices) + u'}')
        string += u'\nBallots Cast:\n' + u'\n'.join(ballots) + u'\n'
        counts_list = []
        for name, points in counts.items():
            counts_list.append(u'%s: %s' % (name, points))
        string += u'\nTotal Counts:\n' + u'\n'.join(counts_list) + u'\n'
    elif pos.position_type == "Boolean-Voting":
        json = pos.to_json()
        string = u"""
Position Name: {0},
Vote Required: {1},
Write-in Slots: {2},
Position Slots: {3},
Candidates: {4},
Winners: {5}""".format(encode(pos.position.name),
                       pos.vote_required,
                       pos.write_in_slots,
                       pos.slots,
                       u', '.join([encode(can.name) for can in pos.election_position_candidates]),
                       u', '.join([encode(db.get(winner).name) for winner in pos.winners]))
        counts = {}
        ballots = []
        for ballot in pos.ballots:
            choices = []
            for choice in ballot.choices:
                choices.append(u'%s: %d' % (choice.candidate.name, choice.points))
                if choice.candidate.name in counts:
                    counts[choice.candidate.name] += choice.points
                else:
                    counts[choice.candidate.name] = choice.points
            ballots.append(u'{' + u', '.join(choices) + u'}')
        string += u'\nBallots Cast:\n' + u'\n'.join(ballots) + u'\n'
        counts_list = []
        for name, points in counts.items():
            counts_list.append(u'%s: %s' % (name, points))
        string += u'\nTotal Counts:\n' + u'\n'.join(counts_list) + u'\n'

    message.body = u"""
Dear {0} Admin,

Voting for {1} has concluded. Below are the detailed results of the election.
""".format(election.organization.name, election.name)
    message.body += u'\nPosition Results\n' + string
    message.body += u'\n\nAt your service,\n\nOwlection Team'
    message.send()

def email_report(to, election):
    """
    Sends an email to the election admin with the results and ballots.
    """
    admins = [organization_admin.admin for organization_admin in
                    election.organization.organization_admins]
    message = mail.EmailMessage(
        sender="no-reply@owlection.appspotmail.com",
        subject="Election Report for %s" % election.name)
    message.to = ', '.join(to)

    results = []
    ranked_positions = models.RankedVotingPosition.gql("WHERE election=:1",
                                                         election)
    logging.info("Number of positions: %d" % ranked_positions.count())
    i = 1
    for pos in ranked_positions:
        logging.info("Processing position", i)
        i += 1
        json = pos.to_json()
        string = (u"\n"
                  u"Position Name: {0},\n"
                  u"Vote Required: {1},\n"
                  u"Write-in Slots: {2},\n"
                  u"Candidates: {3},\n"
                  u"Winners: {4}").format(pos.position.name,
                       pos.vote_required,
                       pos.write_in_slots,
                       u', '.join([encode(can.name) for can in pos.election_position_candidates]),
                       u', '.join([encode(db.get(winner).name) for winner in pos.winners]))
        counts = {}
        ballots = []
        ballots_db = pos.ballots.fetch(100)
        while ballots_db:
            for ballot in ballots_db:
                can_names = [db.get(can).name for can in ballot.preferences]
                ballots.append(u'[' +
                    u', '.join(can_names) +
                    u']')
                if can_names:
                    if can_names[0] in counts:
                        counts[can_names[0]] += 1
                    else:
                        counts[can_names[0]] = 1
            ballots_db = pos.ballots.filter('__key__ >', ballots_db[-1].key()).fetch(100)
        string += u'\nBallots Cast:\n' + u'\n'.join(ballots) + u'\n'
        string += u'Total First Preference Counts: %s' % counts
        results.append(string)

    cumulative_positions = models.CumulativeVotingPosition.gql("WHERE election=:1",
                                                             election)
    for pos in cumulative_positions:
        json = pos.to_json()
        string = (u"""
Position Name: {0}
Vote Required: {1}
Write-in Slots: {2}
Position Slots: {3}
Points per voter: {4}
Candidates: {5}
Winners: {6}""").format(pos.position.name,
                       pos.vote_required,
                       pos.write_in_slots,
                       pos.slots,
                       pos.points,
                       u', '.join([encode(can.name) for can in pos.election_position_candidates]),
                       u', '.join([encode(db.get(winner).name) for winner in pos.winners]))
        counts = {}
        ballots = []
        for ballot in pos.ballots:
            choices = []
            for choice in ballot.choices:
                choices.append(u'%s: %d' % (choice.candidate.name, choice.points))
                if choice.candidate.name in counts:
                    counts[choice.candidate.name] += choice.points
                else:
                    counts[choice.candidate.name] = choice.points
            ballots.append(u'{' + u', '.join(choices) + u'}')
        string += u'\nBallots Cast:\n' + u'\n'.join(ballots) + u'\n'
        counts_list = []
        for name, points in counts.items():
            counts_list.append(u'%s: %s' % (name, points))
        string += u'\nTotal Counts:\n' + u'\n'.join(counts_list) + u'\n'
        results.append(string)

    # Similar code to above
    boolean_positions = models.BooleanVotingPosition.gql("WHERE election=:1",
                                                             election)
    for pos in boolean_positions:
        json = pos.to_json()
        string = (u"""
Position Name: {0}
Vote Required: {1}
Write-in Slots: {2}
Position Slots: {3}
Candidates: {4}
Winners: {5}""").format(pos.position.name,
                       pos.vote_required,
                       pos.write_in_slots,
                       pos.slots,
                       u', '.join([encode(can.name) for can in pos.election_position_candidates]),
                       u', '.join([encode(db.get(winner).name) for winner in pos.winners]))
        counts = {}
        ballots = []
        for ballot in pos.ballots:
            choices = []
            for choice in ballot.choices:
                choices.append(u'%s: %d' % (choice.candidate.name, choice.points))
                if choice.candidate.name in counts:
                    counts[choice.candidate.name] += choice.points
                else:
                    counts[choice.candidate.name] = choice.points
            ballots.append(u'{' + u', '.join(choices) + u'}')
        string += u'\nBallots Cast:\n' + u'\n'.join(ballots) + u'\n'
        counts_list = []
        for name, points in counts.items():
            counts_list.append(u'%s: %s' % (name, points))
        string += u'\nTotal Counts:\n' + u'\n'.join(counts_list) + u'\n'
        results.append(string)

    message.body = u"""
Dear {0} Admin,

Voting for {1} has concluded. Below are the detailed results of the election.
""".format(election.organization.name, election.name)
    message.body += u'\nPosition Results\n' + u'\n'.join(results)
    message.body += u'\n\nAt your service,\n\nOwlection Team'
    logging.info(message.body)
    #print message.body
    message.send()
    logging.info('Message Sent')