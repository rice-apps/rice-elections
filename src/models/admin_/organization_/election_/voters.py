"""
Back end for election panel voters.
"""

__author__ = 'Waseem Ahmad <waseem@rice.edu>'

import json
import logging
import webapp2

from authentication import auth
from google.appengine.api import taskqueue
from google.appengine.api import memcache
from models import models, webapputils
from models.admin_.organization_.election import get_panel

PAGE_URL = '/admin/organization/election/voters'
TASK_URL = '/tasks/admin/organization/election/voters'


class ElectionVotersHandler(webapp2.RequestHandler):

    def get(self):
        # Authenticate user
        voter = auth.get_voter(self)
        status = models.get_admin_status(voter)
        if not status:
            webapputils.render_page(self, '/templates/message',
                {'status': 'Not Authorized', 'msg': MSG_NOT_AUTHORIZED})
            return

        # Get election
        election = auth.get_election()
        if not election:
            panel = get_panel(
                PAGE_NAME,
                {'status': 'Error','msg': 'No election found.'},
                None)
            webapputils.render_page_content(self, PAGE_NAME, panel)
            return

        data = {'id': str(election.key()), 'voters': []}
        evs = models.ElectionVoter.gql('WHERE election=:1', election)
        for ev in evs:
        	data['voters'].append(ev.voter)
        logging.info(data)
        panel = get_panel(PAGE_URL, data, data.get('id'))
        webapputils.render_page_content(self, PAGE_URL, panel)

    def post(self):
        methods = {
            'add_voters': self.add_voters,
            'delete_voters': self.delete_voters
        }

        # Get election
        election = auth.get_election()
        if not election:
            return

        # Verify that the election is not universal
        if election.universal:
            webapputils.respond(self, 'ERROR', 'Universal election')

        # Get the method
        data = json.loads(self.request.get('data'))
        method = data['method']
        logging.info('Method: %s\n Data: %s', method, data)
        if method in methods:
            methods[method](election, data)
        else:
            webapputils.respond(self, 'ERROR', 'Unkown method')

    def add_voters(self, election, data):
        self.voters_task(election, data, 'add_voters')
        webapputils.respond(self, 'OK', 'Adding')

    def delete_voters(self, election, data):
        self.voters_task(election, data, 'delete_voters')
        webapputils.respond(self, 'OK', 'Deleting')

    def voters_task(self, election, data, method):
        queue_data = {'election_key': str(election.key()),
                      'method': method,
                      'voters': data['voters']}
        retry_options = taskqueue.TaskRetryOptions(task_retry_limit=0)
        taskqueue.add(url=TASK_URL,
                      params={'data':json.dumps(queue_data)},
                      retry_options=retry_options)

class ElectionVotersTaskHandler(webapp2.RequestHandler):

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
        

    def delete_voters(self, election, voters):
        models.remove_eligible_voters(election, voters)
        
