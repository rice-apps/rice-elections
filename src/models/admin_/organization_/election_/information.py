"""
Back end for election panel information.
"""

__author__ = 'Waseem Ahmad <waseem@rice.edu>'

import json
import logging
import webapp2

from authentication import auth
from datetime import datetime
from models import models, webapputils
from models.admin_.organization_.election import get_panel

PAGE_NAME = '/admin/organization/election/information'

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
        panel = get_panel(PAGE_NAME, data, data.get('id'))
        webapputils.render_page_content(self, PAGE_NAME, panel)

    def post(self):
        # Authenticate user
        org = auth.get_organization()
        if not org:
            webapputils.respond(self, 'ERROR', 'Not Authorized')
            return

        election = auth.get_election()
        if election:
            data = {'status': 'OK', 'election': election.to_json()}
        else:
            data = {'status': 'OK'}
        logging.info(data)
        self.response.write(json.dumps(data))

class ElectionUpdateHandler(webapp2.RequestHandler):
    def post(self):
        # Authenticate user
        org = auth.get_organization()
        if not org:
            webapputils.respond(self, 'ERROR', 'Not Authorized')
            return

        # Get form data
        formData = self.request.get('formData')
        data = json.loads(formData)
        logging.info(data)
        if not formData:
            webapputils.respond(self, 'ERROR', 'No Form Data Sent!')
            return

        election = auth.get_election()
        out = {'status': 'OK'}
        if not election:
            # User must be trying to create new election
            election = models.Election(
                name=data['name'],
                start=datetime.fromtimestamp(data['times']['start']),
                end=datetime.fromtimestamp(data['times']['end']),
                organization=org,
                universal=data['universal'],
                result_delay=data['result_delay'])
            election.put()
            election.clear_cache()
            out['msg'] = 'Created'
            auth.set_election(election)
        else:
            election.name = data['name']
            election.start = datetime.fromtimestamp(data['times']['start'])
            election.end = datetime.fromtimestamp(data['times']['end'])
            election.universal = data['universal']
            election.result_delay = data['result_delay']
            election.put()
            election.clear_cache()
            out['msg'] = 'Updated'
        out['election'] = election.to_json()
        self.response.write(json.dumps(out))
