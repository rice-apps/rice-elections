"""
Back-end for serving and accepting a ballot for an election.
"""

__authors__ = ['Waseem Ahmad (waseem@rice.edu)', 'Andrew Capshaw (capshaw@rice.edu)']

import datetime
import database
import logging
import random
import webapp2

from main import render_page, require_login

class BallotHandler(webapp2.RequestHandler):
    """
    Handles GET requests for the Vote page.
    """

    def get(self):
        page_data = {}

        # Authenticate user
        net_id = require_login(self)
        voter = database.get_voter(net_id)
        if not voter:
            render_page(self, '/vote', page_data)
            return
        
        # Serve the election the user has requested

        render_page(self, '/vote', page_data)


app = webapp2.WSGIApplication([
        ('/cast-ballot', BallotHandler)
], debug=True)