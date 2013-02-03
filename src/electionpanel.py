"""
Back-end for the Election Panel.
"""

__author__ = 'Waseem Ahmad <waseem@rice.edu>'

import database
import json
import logging
import webapp2

from authentication import require_login, get_voter
from datetime import datetime, timedelta
from google.appengine.api import taskqueue
from google.appengine.ext import db
from main import render_html, render_page

PAGE_NAME = '/election-panel'
MSG_NOT_AUTHORIZED = ('We\'re sorry, you\'re not an organization administrator. Please contact the website administration '
                     'if you are interested in conducting elections for your organization.')

class AdminHandler(webapp2.RequestHandler):
    
    def get(self):
        # Authenticate user
        voter = get_voter()
        if not voter:
            require_login(self)
        status = database.get_admin_status(voter)
        if not status:
            render_page(self, '/message', {'status': 'Not Authorized', 'msg': MSG_NOT_AUTHORIZED})
            return

        # Get organization information
        admin = database.Admin.gql('WHERE voter=:1', voter).get()
        org_admin = database.OrganizationAdmin.gql('WHERE admin=:1',
                                                    admin).get()
        org = org_admin.organization

        # Construct page information
        page_data = {}
        page_data['id'] = self.request.get('id')
        
        render_page(self, PAGE_NAME, page_data)

    def post(self):
        data = json.loads(self.request.get('data'))
        method = data['method']
        election_id = data['id']
        election = {}
        if election_id:
            election_entry = database.Election.get(election_id)
            election = election_entry.to_json()
        render_html(self, '/election-panel-information', election)
        return None
        
app = webapp2.WSGIApplication([
        ('/election-panel', AdminHandler)
], debug=True)