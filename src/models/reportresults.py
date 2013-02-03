"""
Script to report election results including ballots in detail to election admin.
"""

__author__ = 'Waseem Ahmad <waseem@rice.edu>'


import models
import logging
import webapp2

from google.appengine.ext import db
from google.appengine.api import mail
from datetime import datetime

def encode(string):
	return string.encode('ascii', 'replace')

def email_report(election):
	"""
	Sends an email to the election admin with the results and ballots.
	"""
	admins = [organization_admin.admin for organization_admin in
					election.organization.organization_admins]
	message = mail.EmailMessage(
		sender="no-reply@owlection.appspotmail.com",
		subject="Election Report for %s" % election.name)
	message.to = ', '.join([admin.email for admin in admins])

	results = []
	ranked_positions = models.RankedVotingPosition.gql("WHERE election=:1",
														 election)
	for pos in ranked_positions:
		json = pos.to_json()
		string = """
Position Name: {0},
Vote Required: {1},
Write-in Slots: {2},
Candidates: {3},
Winners: {4}""".format(pos.position.name,
					   pos.vote_required,
					   pos.write_in_slots,
					   ', '.join([encode(can.name) for can in pos.election_position_candidates]),
					   ', '.join([encode(db.get(winner).name) for winner in pos.winners]))
		ballots = []
		for ballot in pos.ballots:
			ballots.append('[' +
				', '.join([db.get(can).name for can in ballot.preferences]) +
				']')
		string += '\nBallots Cast:\n' + '\n'.join(ballots) + '\n'
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
					   ', '.join([encode(can.name) for can in pos.election_position_candidates]),
					   ', '.join([encode(db.get(winner).name) for winner in pos.winners]))
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
	message.send()

