"""
Back end for election panel information.
"""

__author__ = 'Waseem Ahmad <waseem@rice.edu>'

import json
import logging
import webapp2

from authentication import auth
from datetime import datetime, timedelta
from google.appengine.api import taskqueue
from models import models, webapputils, report_results
from models.admin_.organization_.election import get_panel

PAGE_URL = '/admin/organization/election/information'
TASK_URL = '/tasks/admin/organization/election/information'

class ElectionInformationHandler(webapp2.RequestHandler):

    def get(self):
        # Authenticate user
        voter = auth.get_voter(self)
        status = models.get_admin_status(voter)
        if not status:
            webapputils.render_page(self, '/templates/message', 
                {'status': 'Error', 'msg': 'Not Authorized'})
            return
        
        data = {}

        # Get election
        election = auth.get_election()
        if election:
            data = {'id': str(election.key()),
                    'election': election.to_json()}
        panel = get_panel(PAGE_URL, data, data.get('id'))
        webapputils.render_page_content(self, PAGE_URL, panel)

    def post(self):
        methods = {
            'get_election': self.get_election,
            'update_election': self.update_election
        }

        # Authenticate user
        org = auth.get_active_organization()
        if not org:
            webapputils.respond(self, 'ERROR', 'Not Authorized')
            return

        # Get election
        election = auth.get_election()

        # Get the method
        data = json.loads(self.request.get('data'))
        method = data['method']
        logging.info('Method: %s\n Data: %s', method, data)
        if method in methods:
            methods[method](election, data)
        else:
            webapputils.respond(self, 'ERROR', 'Unkown method')

    def get_election(self, election, data):
        out = {'status': 'OK'}
        if election:
            out['election'] = election.to_json()
        self.response.write(json.dumps(out))

    def update_election(self, election, data):
        out = {'status': 'OK'}
        end_dt = datetime.fromtimestamp(data['times']['end'])
        pub_dt = datetime.fromtimestamp(data['times']['pub'])
        # delay = difference between pub and end in seconds
        res_delay = int((pub_dt - end_dt).total_seconds())
        if not election:
            # User must be trying to create new election
            election = models.Election(
                name=data['name'],
                start=datetime.fromtimestamp(data['times']['start']),
                end=end_dt,
                organization=auth.get_active_organization(),
                universal=data['universal'],
                hidden=data['hidden'],
                result_delay=res_delay,
                description=data['description'])
            election.put()
            out['msg'] = 'Created'
            auth.set_election(election)
        else:
            election.name = data['name']
            election.start = datetime.fromtimestamp(data['times']['start'])
            election.end = end_dt
            election.universal = data['universal']
            election.hidden = data['hidden']
            election.result_delay = res_delay
            election.description = data['description']
            election.put()
            out['msg'] = 'Updated'
        out['election'] = election.to_json()
        self.response.write(json.dumps(out))


