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
    return string.encode('ascii', 'replace')

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
        string = """
Position Name: {0},
Vote Required: {1},
Write-in Slots: {2},
Candidates: {3},
Winners: {4}""".format(pos.position.name,
                       pos.vote_required,
                       pos.write_in_slots,
                       ', '.join([encode(can.name.decode('utf-8', 'replace')) for can in pos.election_position_candidates]),
                       ', '.join([encode(db.get(winner).name.decode('utf-8', 'replace')) for winner in pos.winners]))
    
        counts = {}
        ballots = []
        for ballot in pos.ballots:
            can_names = [db.get(can).name for can in ballot.preferences]
            ballots.append('[' + ','.join(can_names) + ']')
            if can_names:
                if can_names[0] in counts:
                    counts[can_names[0]] += 1
                else:
                    counts[can_names[0]] = 1
        string += '\nBallots Cast:\n' + '\n'.join(ballots) + '\n'
        string += 'Total First Preference Counts: %s' % counts
    elif pos.position_type == "Cumulative-Voting":
        json = pos.to_json()
        string = """
Position Name: {0},
Vote Required: {1},
Write-in Slots: {2},
Position Slots: {3},
Points per voter: {4},
Candidates: {5},
Winners: {6}""".format(encode(pos.position.name.decode('utf-8', 'replace')),
                       pos.vote_required,
                       pos.write_in_slots,
                       pos.slots,
                       pos.points,
                       ', '.join([encode(can.name.decode('utf-8', 'replace')) for can in pos.election_position_candidates]),
                       ', '.join([encode(db.get(winner).name.decode('utf-8', 'replace')) for winner in pos.winners]))
        counts = {}
        ballots = []
        for ballot in pos.ballots:
            choices = []
            for choice in ballot.choices:
                choices.append('%s: %d' % (choice.candidate.name, choice.points))
                if choice.candidate.name in counts:
                    counts[choice.candidate.name] += choice.points
                else:
                    counts[choice.candidate.name] = choice.points
            ballots.append('{' + ', '.join(choices) + '}')
        string += '\nBallots Cast:\n' + '\n'.join(ballots) + '\n'
        counts_list = []
        for name, points in counts.items():
            counts_list.append('%s: %s' % (name, points))
        string += '\nTotal Counts:\n' + '\n'.join(counts_list) + '\n'

    message.body = """
Dear {0} Admin,

Voting for {1} has concluded. Below are the detailed results of the election.
""".format(election.organization.name, election.name)
    message.body += '\nPosition Results\n' + string
    message.body += '\n\nAt your service,\n\nOwlection Team'
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
    print "Number of positions: %d" % ranked_positions.count()
    i = 1
    for pos in ranked_positions:
        print "Processing position", i
        i += 1
        json = pos.to_json()
        string = """
Position Name: {0},
Vote Required: {1},
Write-in Slots: {2},
Candidates: {3},
Winners: {4}""".format(pos.position.name,
                       pos.vote_required,
                       pos.write_in_slots,
                       ', '.join([encode(can.name.decode('utf-8', 'replace')) for can in pos.election_position_candidates]),
                       ', '.join([encode(db.get(winner).name.decode('utf-8', 'replace')) for winner in pos.winners]))
        counts = {}
        ballots = []
        ballots_db = pos.ballots.fetch(100)
        while ballots_db:
            for ballot in ballots_db:
                can_names = [db.get(can).name for can in ballot.preferences]
                ballots.append('[' +
                    ', '.join(can_names) +
                    ']')
                if can_names:
                    if can_names[0] in counts:
                        counts[can_names[0]] += 1
                    else:
                        counts[can_names[0]] = 1
            ballots_db = pos.ballots.filter('__key__ >', ballots_db[-1].key()).fetch(100)
        string += '\nBallots Cast:\n' + '\n'.join(ballots) + '\n'
        string += 'Total First Preference Counts: %s' % counts
        results.append(string)

    cumulative_positions = models.CumulativeVotingPosition.gql("WHERE election=:1",
                                                             election)
    for pos in cumulative_positions:
        json = pos.to_json()
        string = """
Position Name: {0},
Vote Required: {1},
Write-in Slots: {2},
Position Slots: {3},
Points per voter: {4},
Candidates: {5},
Winners: {6}""".format(pos.position.name,
                       pos.vote_required,
                       pos.write_in_slots,
                       pos.slots,
                       pos.points,
                       ', '.join([encode(can.name.decode('utf-8', 'replace')) for can in pos.election_position_candidates]),
                       ', '.join([encode(db.get(winner).name.decode('utf-8', 'replace')) for winner in pos.winners]))
        counts = {}
        ballots = []
        for ballot in pos.ballots:
            choices = []
            for choice in ballot.choices:
                choices.append('%s: %d' % (choice.candidate.name, choice.points))
                if choice.candidate.name in counts:
                    counts[choice.candidate.name] += choice.points
                else:
                    counts[choice.candidate.name] = choice.points
            ballots.append('{' + ', '.join(choices) + '}')
        string += '\nBallots Cast:\n' + '\n'.join(ballots) + '\n'
        counts_list = []
        for name, points in counts.items():
            counts_list.append('%s: %s' % (name, points))
        string += '\nTotal Counts:\n' + '\n'.join(counts_list) + '\n'
        results.append(string)

    message.body = """
Dear {0} Admin,

Voting for {1} has concluded. Below are the detailed results of the election.
""".format(election.organization.name, election.name)
    message.body += '\nPosition Results\n' + '\n'.join(results)
    message.body += '\n\nAt your service,\n\nOwlection Team'
    logging.info(message.body)
    print message.body
    message.send()

