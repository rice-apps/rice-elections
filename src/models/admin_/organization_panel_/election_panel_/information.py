"""
Back end for election panel information.
"""

__author__ = 'Waseem Ahmad <waseem@rice.edu>'

import webapp2

from authentication import auth
from main import render_page_content
from models import models
from models.admin_.organization_panel_.election_panel import get_panel

PAGE_NAME = '/admin/organization-panel/election-panel/information'

class ElectionInformationHandler(webapp2.RequestHandler):

    def get(self):
        # Authenticate user
        voter = auth.get_voter(self)
        status = models.get_admin_status(voter)
        if not status:
            render_page(self, '/templates/message', {'status': 'Not Authorized', 'msg': MSG_NOT_AUTHORIZED})
            return
        
        # Get election
        election_id = self.request.get('id')
        data = {'id': election_id}
        if election_id:
            data['election'] = models.Election.get(election_id).to_json()
        panel = get_panel(PAGE_NAME, data, election_id)
        render_page_content(self, PAGE_NAME, panel)
