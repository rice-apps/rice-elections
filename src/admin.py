"""
Back-end for the Admin.
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
from main import render_page

PAGE_NAME = '/admin'
MSG_NOT_AUTHORIZED = ('We\'re sorry, you\'re not an election administrator. Please contact the website administration '
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
            if voter.net_id != 'wa1':
                return
            # TODO: Temp hard-code
            for new_net_id, new_email in {'wa1': 'wa1@rice.edu', 'jcc7': 'jcc7@rice.edu', 'apc1': 'apc1@rice.edu'}.items():
                voter = database.get_voter(new_net_id, create=True)
                organization = database.get_organization('Brown College')
                database.put_admin(voter, new_email, organization)
            return
        
        render_page(self, PAGE_NAME, {})

    def respond(self, status, message):
        """
        Sends a response to the front-end.
        
        Args:
            status: response status
            message: response message
        """
        self.response.write(json.dumps({'status': status, 'msg': message}))
        
app = webapp2.WSGIApplication([
        ('/admin', AdminHandler)
], debug=True)