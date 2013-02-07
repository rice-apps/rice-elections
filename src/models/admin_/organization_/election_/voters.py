"""
Back end for election panel voters.
"""

__author__ = 'Waseem Ahmad <waseem@rice.edu>'

import webapp2

from authentication import auth
from models import models, webapputils
from models.admin_.organization_.election import get_panel

PAGE_NAME = '/admin/organization/election/voters'

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
        election_id = self.request.get('id')
        data = {'voters': [], 'id': election_id}
        if election_id:
            election = models.Election.get(election_id)
            evs = models.ElectionVoter.gql('WHERE election=:1', election)
            for election_voter in evs:
            	data['voters'].append(election_voter.voter)
        panel = get_panel(PAGE_NAME, data, election_id)
        webapputils.render_page_content(self, PAGE_NAME, panel)
