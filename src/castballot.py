"""
Back-end for serving and accepting a ballot for an election.
"""

__authors__ = ['Waseem Ahmad (waseem@rice.edu)', 'Andrew Capshaw (capshaw@rice.edu)']

import json
import logging
import random
import webapp2

from authentication import require_login
from gaesessions import get_current_session
from google.appengine.ext import db
from main import render_page

PAGE_NAME = '/cast-ballot'


class BallotHandler(webapp2.RequestHandler):
    """
    Handles GET requests for the Vote page.
    """

    def get(self):
        """
        Serves the empty ballot to the client-side so that the user may fill it out and submit it back via post.
        """
        page_data = {}

        # Authenticate user
        session = get_current_session()
        if not session.has_key('voter'):
            require_login(self)
        
        voter = session['voter']
        net_id = voter.net_id
        
        # Serve the election the user has requested
        election_id = self.request.get('id')
        if not election_id:
            page_data['error_msg'] = 'No election was specified.'
            render_page(self, PAGE_NAME, page_data)
            return
        logging.info('%s requested election: %s', net_id, election_id)

        # Get the election from the database
        election = db.get(election_id)
        if not election:
            page_data['error_msg'] = 'Election not found.'
            render_page(self, PAGE_NAME, page_data)
            return

        # Make sure user is eligible to vote
        if not voter or election.key() not in voter._election_keys:
            page_data['error_msg'] = 'You are not eligible to vote for this election.'
            render_page(self, PAGE_NAME, page_data)
            return

        # Write election information
        page_data['id'] = str(election.key())
        page_data['name'] = election.name
        page_data['organization'] = election.organization.name
        page_data['positions'] = []
        page_data['voter_net_id'] = voter.net_id

        # Write position information
        election_positions = election.election_positions
        for election_position in election_positions:
            position = {}
            position['id'] = str(election_position.key())
            position['name'] = election_position.position.name
            position['slots'] = election_position.slots
            position['type'] = election_position.type
            position['write_in'] = election_position.write_in
            position['vote_required'] = election_position.vote_required
            position['candidates'] = []
            for candidate_key in election_position.candidates:
                candidate = db.get(candidate_key)
                position['candidates'].append({'name': candidate.name,
                                               'id': str(candidate_key)})
            random.shuffle(position['candidates'])
            page_data['positions'].append(position)

        logging.info(page_data)

        render_page(self, PAGE_NAME, page_data)
    
    def post(self):
        """
        Takes the filled out ballot from the client-side, validates it, and stores it in the database.
        Sends confirmation to client-side.
        """
        logging.info('Received new ballot submission.')
        
        # Authenticate user
#        net_id = require_login(self)
#        logging.info('User: %s', net_id)
        
        
        logging.info(self.request.POST)
        self.respond('OK', 'We got your ballot. Now go home!')
        
    def respond(self, status, message):
        """
        Sends a response to the front-end.
        
        Args:
            status: response status
            message: response message
        """
        self.response.write(json.dumps({'status': status, 'msg': message}))
    
app = webapp2.WSGIApplication([
        ('/cast-ballot', BallotHandler)
], debug=True)