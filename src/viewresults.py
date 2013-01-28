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
        if status != 'invalid_time' and not database.get_admin_status(voter, election.organization):
            page_data['error_msg'] = 'You are not eligible to view results.'
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
                                         'Please wait for %s longer.' % 
                                         str(public_result_time - datetime.now())[:4])
                render_page(self, PAGE_NAME, page_data)
                return

        # Write election information
        for key, value in election.to_json().items():
            page_data[key] = value
        page_data['voter_net_id'] = voter.net_id
        page_data['positions'] = []
        
        # Write position information
        election_positions = election.election_positions
        for election_position in election_positions:
            position = {}
            for key, value in election_position.to_json().items():
                position[key] = value
            page_data['positions'].append(position)

        logging.info(page_data)

        render_page(self, PAGE_NAME, page_data)

app = webapp2.WSGIApplication([
        ('/view-results', ResultsHandler)
], debug=True)