"""
Performs scheduled or heavy tasks that are not within the scope of a normal
web request.
"""

__author__ = 'Waseem Ahmad <waseem@rice.edu>'

import logging
import json
import reportresults
import webapp2

from datetime import datetime
from google.appengine.api import mail
from models import models

class ElectionVoterFactory(webapp2.RequestHandler):
    """
    Adds a list of ElectionVoters for a given election.
    """
    def post(self):
        data = json.loads(self.request.get('data'))
        election_key = data['election_key']
        election = models.Election.get(election_key)
        voters = data['voter_list']
        if election and voters:
            models.add_eligible_voters(election, voters)
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

class ElectionResultsFactory(webapp2.RequestHandler):
    """
    Computes the results for a given election.
    """
    def post(self):
        data = json.loads(self.request.get('data'))
        election_key = data['election_key']
        election = models.Election.get(election_key)

        # Assert validity
        if not election:
            logging.error('Election not found.')
            return
        if election.end > datetime.now():
            logging.error('Election is still open.')
            return
        if election.result_computed:
            logging.error('Election results already computed.')
            return

        logging.info('Computing results for election: %s, organization: %s.', 
                        election.name, election.organization.name)

        for election_position in election.election_positions:
            logging.info('Computing election position: %s',
                            election_position.position.name)
            election_position.compute_winners()

        election.result_computed = True
        election.put()
        logging.info('Computed results for election: %s, organization: %s.',
                        election.name, election.organization.name)
        reportresults.email_report(election)

app = webapp2.WSGIApplication([
    ('/tasks/election-voter-factory', ElectionVoterFactory),
    ('/tasks/election-results-factory', ElectionResultsFactory)],
    debug=True)