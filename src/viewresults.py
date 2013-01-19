"""
Back-end for serving the results of an election.
"""

__authors__ = ['Waseem Ahmad (waseem@rice.edu)', 'Andrew Capshaw (capshaw@rice.edu)']

import database
import logging
import webapp2

from authentication import require_login, get_voter
from datetime import datetime, timedelta
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
        election = database.Election.get(election_id)
        if not election:
            page_data['error_msg'] = 'Election not found.'
            render_page(self, PAGE_NAME, page_data)
            return
        
        # Make sure user is eligible to vote
        status = database.voter_status(voter, election)
        if status != 'eligible' and not database.get_admin_status(voter, election.organization):
            render_page(self, PAGE_NAME, page_data)
            return
        
        if not election.result_computed:
            page_data['error_msg'] = 'Election results are not available yet.'
            render_page(self, PAGE_NAME, page_data)
            return
        
        public_result_time = election.end
        if election.result_delay:
            public_result_time += timedelta(seconds=election.result_delay)
            
        if datetime.now() < public_result_time:
            # Check to see if the user is an election admin
            status = database.get_admin_status(voter, election.organization)
            if not status:
                page_data['error_msg'] = ('Election results are not available to the public yet. '
                                         'Please wait for %s longer.' % (public_result_time - datetime.now()))
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
            position['candidates'] = []
            for election_position_candidate in election_position.election_position_candidates:
                candidate = election_position_candidate.candidate
                position['candidates'].append({'name': candidate.name,
                                               'id': str(election_position_candidate.key()),
                                               'won': election_position_candidate.winner}) # TODO: temp random
            page_data['positions'].append(position)

        logging.info(page_data)

        render_page(self, PAGE_NAME, page_data)

app = webapp2.WSGIApplication([
        ('/view-results', ResultsHandler)
], debug=True)