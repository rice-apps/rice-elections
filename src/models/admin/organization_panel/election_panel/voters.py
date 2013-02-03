"""
Back end for election panel voters.
"""

__author__ = 'Waseem Ahmad <waseem@rice.edu>'

import models
import webapp2

from authentication import require_login, get_voter
from main import render_page_content
from models.admin.organization_panel.election_panel import get_panel

PAGE_NAME = '/admin/organization-panel/election-panel/voters'

class ElectionVotersHandler(webapp2.RequestHandler):

    def get(self):
        # Authenticate user
        voter = get_voter()
        if not voter:
            require_login(self)
        status = models.get_admin_status(voter)
        if not status:
            render_page(self, '/message', {'status': 'Not Authorized', 'msg': MSG_NOT_AUTHORIZED})
            return
        
        # Get election
        election_id = self.request.get('id')
        data = {'voters': [], 'id': election_id}
        if election_id:
            election = models.Election.get(election_id)
            evs = models.ElectionVoter.gql('WHERE election=:1', election)
            for election_voter in evs:
            	data['voters'].append(election_voter.voter)
        panel = get_panel(PAGE_NAME, data, election_id)
        render_page_content(self, PAGE_NAME, panel)
