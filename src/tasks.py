"""
Performs scheduled or heavy tasks that are not within the scope of a normal
web request.
"""

__author__ = 'Waseem Ahmad <waseem@rice.edu>'

import database
import logging
import json
import webapp2

from google.appengine.api import mail

class ElectionVoterFactory(webapp2.RequestHandler):
	"""
	Adds a list of ElectionVoters for a given election.
	"""
	def post(self):
		data = json.loads(self.request.get('data'))
		election_key = data['election_key']
		election = database.Election.get(election_key)
		voters = data['voter_list']
		if election and voters:
			database.add_eligible_voters(election, voters)
		else:
			logging.error('Task Error, database or voters could not be found.')
			return

		# Email Success
		admins = [org_admin.admin for org_admin in 
					election.organization.organization_admins]
		message = mail.EmailMessage(
			sender="no-reply@owlection.appspotmail.com",
			subject="Eligible Voters added for %s" % election.name)
		message.to = ', '.join([admin.email for admin in admins])
		message.body = ('Dear {0} Admin,\n\n'
			'The eligible voters specified for {1} have been successfully'
			' added. The total number of voters added is {2}.\n\n'
			'At your service,\n\n'
			'Owlection Team').format(election.organization.name,
						 			election.name,
						 			len(voters))
		logging.info(message.body)
		message.send()


app = webapp2.WSGIApplication([
	('/tasks/election-voter-factory', ElectionVoterFactory)],
	debug=True)