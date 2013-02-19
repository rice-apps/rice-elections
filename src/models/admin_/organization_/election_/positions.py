"""
Back end for election panel positions.
"""

__author__ = 'Waseem Ahmad <waseem@rice.edu>'

import json
import logging
import webapp2

from authentication import auth
from models import models, webapputils
from models.admin_.organization_.election import get_panel

PAGE_NAME = '/admin/organization/election/positions'


class ElectionPositionsHandler(webapp2.RequestHandler):

    def get(self):
        # Authenticate user
        voter = auth.get_voter(self)
        status = models.get_admin_status(voter)
        if not status:
            webapputils.render_page(self, '/templates/message',
                {'status': 'Error', 'msg': 'Not Authorized'})
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

        data = {'id': str(election.key())}
        panel = get_panel(PAGE_NAME, data, data.get('id'))
        webapputils.render_page_content(self, PAGE_NAME, panel)

    def post(self):
        methods = {
            'get_elections': self.get_elections
        }

        # Get election
        election = auth.get_election()
        if not election:
            return

        # Get the method
        data = json.loads(self.request.get('data'))
        method = data['method']
        logging.info('Method: %s Data: %s', method, data)
        if method in methods:
            methods[method](election, data)

    def get_elections(self, election, data):
        data = {'elections': [p.to_json() for p in election.election_positions]}
        self.response.write(json.dumps(data))