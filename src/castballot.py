"""
Back-end for serving and accepting a ballot for an election.
"""

__authors__ = ['Waseem Ahmad (waseem@rice.edu)', 'Andrew Capshaw (capshaw@rice.edu)']

import database
import logging
import webapp2

from main import render_page, require_login
from google.appengine.ext import db

PAGE_NAME = '/cast-ballot'


class BallotHandler(webapp2.RequestHandler):
    """
    Handles GET requests for the Vote page.
    """

    def get(self):
        page_data = {}

        # Authenticate user
        net_id = require_login(self)
        
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
        voter = database.get_voter(net_id)
        if not voter or election.key() not in voter._election_keys:
            page_data['error_msg'] = 'You are not eligible to vote for this election.'
            render_page(self, PAGE_NAME, page_data)
            return
        
        # Write election information
        page_data['name'] = election.name
        page_data['organization'] = election.organization.name
        page_data['positions'] = []
        
        # Write position information
        election_positions = election.election_positions
        for election_position in election_positions:
            position = {}
            position['name'] = election_position.position.name
            position['slots'] = election_position.slots
            position['type'] = election_position.type
            position['write_in'] = election_position.write_in
            position['candidates'] = []
            for candidate_key in election_position.candidates:
                candidate = db.get(candidate_key)
                position['candidates'].append(candidate.name)
            page_data['positions'].append(position)
        
        logging.info(page_data)
        
        render_page(self, PAGE_NAME, page_data)


app = webapp2.WSGIApplication([
        ('/cast-ballot', BallotHandler)
], debug=True)