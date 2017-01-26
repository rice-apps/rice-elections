"""
Performs scheduled or heavy tasks that are not within the scope of a normal
web request.
"""

__author__ = 'Waseem Ahmad <waseem@rice.edu>'

import logging
import json
import webapp2
from models import models, report_results, new_results

from datetime import datetime, timedelta
from google.appengine.api import mail, taskqueue
from google.appengine.ext import deferred


def compute_results(election):
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

    total_ballot_count = 0
    for election_position in election.election_positions:
        total_ballot_count += election_position.ballots.count()
    if total_ballot_count > 2500:
        large_election = True
    else:
        large_election = False

    all_computed = True
    for election_position in election.election_positions:
        if not election_position.result_computed:
            all_computed = False

            if large_election:
                logging.info('Found Large Election. Enqueueing Position.')
                # Enqueue a task for computing results
                task_name = 'compute-result-' + str(election_position.key()) + 'banana'
                retry_options = taskqueue.TaskRetryOptions(task_retry_limit=0)
                taskqueue.add(
                    name=task_name,
                    url='/tasks/position-results',
                    params={
                        'election_position_key': str(election_position.key())},
                    retry_options=retry_options,
                    queue_name='election-results',
                    target='task-manager'
                )
            else:
                election_position.compute_winners()

    if all_computed:
        election.result_computed = True
        election.put()
        logging.info('Computed results for election: %s, organization: %s.',
                        election.name, election.organization.name)


        if not large_election:
            admin_emails = ['stl2@rice.edu']
            for org_admin in election.organization.organization_admins:
                admin_emails.append(org_admin.admin.email)
            new_results.email_election_results(admin_emails, election)
            election.result_emailed = True


class ElectionResultsHandler(webapp2.RequestHandler):

    def get(self):
        finished_elections = models.Election.gql(
            "WHERE end < :1 AND result_computed = :2", datetime.now(), False).fetch(None)

        if len(finished_elections) > 0:
            for election in finished_elections:
                deferred.defer(compute_results, election, _queue="election-results", _target="task-manager")


class PositionResultsHandler(webapp2.RequestHandler):

    def post(self):
        # Get data 
        elec_pos = models.ElectionPosition.get(
            self.request.get('election_position_key'))
        elec_pos.compute_winners()

        elec = elec_pos.election

        admin_emails = ['stl2@rice.edu']
        for org_admin in elec_pos.election.organization.organization_admins:
            admin_emails.append(org_admin.admin.email)

        new_results.email_election_results(admin_emails, elec, elec_pos)


class ElectionVotersHandler(webapp2.RequestHandler):

    def post(self):
        methods = {
            'add_voters': self.add_voters,
            'delete_voters': self.delete_voters
        }

        # Get data
        data = json.loads(self.request.get('data'))
        election = models.Election.get(data['election_key'])
        voters = data['voters']
        method = data['method']

        # Get the method
        if method in methods:
            methods[method](election, voters)
        else:
            logging.error('Unknown method: %s. Task failed!', method)

    def add_voters(self, election, voters):
        models.add_eligible_voters(election, voters)
        models.update_voter_set(election)

    def delete_voters(self, election, voters):
        models.remove_eligible_voters(election, voters)
        models.update_voter_set(election)


class StartHandler(webapp2.RequestHandler):

    def get(self):
        # respond everything is okay
        self.response.write('Background Started')


app = webapp2.WSGIApplication([
    ('/tasks/election-results', ElectionResultsHandler),
    ('/tasks/position-results', PositionResultsHandler),
    ('/tasks/election-voters', ElectionVotersHandler),
    ('/_ah/start', StartHandler)
], debug=True)
