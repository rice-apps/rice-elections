"""
Performs scheduled or heavy tasks that are not within the scope of a normal
web request.
"""

__author__ = 'Waseem Ahmad <waseem@rice.edu>'

import logging
import json
import webapp2
import models
import report_results

from datetime import datetime, timedelta
from google.appengine.api import mail
from google.appengine.api import taskqueue

TASK_URL = '/tasks/election-results-factory'

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

        admin_emails = []
        for org_admin in election.organization.organization_admins:
            admin_emails.append(org_admin.admin.email)
        report_results.email_report(admin_emails, election)

class ElectionResultsScheduler(webapp2.RequestHandler):

    def get(self):
        finished_elections = models.Election.gql(
            "WHERE end < :1 AND result_computed = :2", datetime.now(), False)

        for election in finished_elections:
            self.schedule_result_computation(election)

    def schedule_result_computation(self, election):
        method_name = "compute_results"
        task_name = str(election.key()) + "-" + method_name

        # Enqueue new task for computing results after election ends
        compute_time = election.end + timedelta(seconds=5)
        data = {'election_key': str(election.key()),
                'method': method_name}
        retry_options = taskqueue.TaskRetryOptions(task_retry_limit=0)
        taskqueue.add(name=task_name,
                      url=TASK_URL,
                      params={'data': json.dumps(data)},
                      eta=compute_time,
                      retry_options=retry_options)
        logging.info('Election result computation enqueued.')

app = webapp2.WSGIApplication([
    (TASK_URL, ElectionResultsFactory),
    ('/tasks/election-results-scheduler', ElectionResultsScheduler)],
    debug=True)