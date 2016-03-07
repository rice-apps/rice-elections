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
TASK_URL = '/tasks/election-voters'


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
                PAGE_URL,
                {'status': 'ERROR','msg': 'No election found.'},
                None)
            webapputils.render_page_content(self, PAGE_URL, panel)
            return

        if election.universal:
            panel = get_panel(
                PAGE_URL,
                {'status': 'Universal Election',
                 'msg': 'This is a universal election, anyone with a valid '
                        'NetID can vote for. Therefore you cannot manage '
                        'the voters list.'},
                None)
            webapputils.render_page_content(self, PAGE_URL, panel)
            return

        data = {'status': 'OK',
                'id': str(election.key()),
                'voters': list(models.get_voter_set(election))}
                #'voters': sorted(list(models.get_voter_set(election)))}
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
        voter_set = models.get_voter_set(election)
        for voter in data['voters']:
            voter_set.add(voter)
        out = {'status': 'OK',
               'msg': 'Adding',
               'voters': sorted(list(voter_set))}
        self.response.write(json.dumps(out))

    def delete_voters(self, election, data):
        self.voters_task(election, data, 'delete_voters')
        voter_set = models.get_voter_set(election)
        for voter in data['voters']:
            voter_set.discard(voter)
        out = {'status': 'OK',
               'msg': 'Deleting',
               'voters': sorted(list(voter_set))}
        self.response.write(json.dumps(out))

    def voters_task(self, election, data, method):
        queue_data = {'election_key': str(election.key()),
                      'method': method,
                      'voters': data['voters']}
        retry_options = taskqueue.TaskRetryOptions(task_retry_limit=0)
        taskqueue.add(url=TASK_URL,
                      queue_name='voters',
                      params={'data': json.dumps(queue_data)},
                      retry_options=retry_options,
                      target='task-manager')

