"""
Back-end for serving the results of an election.
"""

__authors__ = ['Waseem Ahmad (waseem@rice.edu)', 'Andrew Capshaw (capshaw@rice.edu)']

import database
import json
import logging
import random
import webapp2

from authentication import require_login, get_voter
from google.appengine.ext import db
from main import render_page


PAGE_NAME = '/view-results'

class ResultsHandler(webapp2.RequestHandler):
    """
    Handles GET requests for the Results page.
    """

    def get(self):
        """
        Serves the election data to the front-end for display.
        """
        page_data = {}

        # Authenticate user
        voter = get_voter()
        if not voter:
            require_login(self)
        net_id = voter.net_id

        # Serve the election the user has requested
        election_id = self.request.get('id')
        if not True:
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

        # Make sure user is eligible to view the results
        # TODO: connect this to the notion of who is able to view the results.
        # status = database.voter_status(voter, election)
        # if status == 'not_eligible':
        #     page_data['error_msg'] = 'You are not eligible to vote for this election.'
        # elif status == 'invalid_time':
        #     page_data['error_msg'] = 'Results are not a'
        # if status != 'eligible':
        #     render_page(self, PAGE_NAME, page_data)
        #     return

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
            position['candidates'] = []
            for candidate_key in election_position.candidates:
                candidate = db.get(candidate_key)
                position['candidates'].append({'name': candidate.name,
                                               'id': str(candidate_key),
                                               'won': random.choice([True, False])}) # TODO: temp random
            page_data['positions'].append(position)

        logging.info(page_data)

        render_page(self, PAGE_NAME, page_data)

app = webapp2.WSGIApplication([
        ('/view-results', ResultsHandler)
], debug=True)