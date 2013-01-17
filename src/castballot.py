"""
Back-end for serving and accepting a ballot for an election.
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
        voter = get_voter()
        if not voter:
            require_login(self)
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
        status = database.voter_status(voter, election)
        if status == 'voted':
            page_data['error_msg'] = 'You have already voted for this election.'
        elif status == 'not_eligible':
            page_data['error_msg'] = 'You are not eligible to vote for this election.'
        elif status == 'invalid_time':
            page_data['error_msg'] = 'You are not in the eligible voting time for this election.'
        if status != 'eligible':
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
        logging.info(self.request.POST)
        
        formData = json.loads(self.request.get('formData'))
        logging.info(formData)
        
        # Authenticate user
        voter = get_voter()
        if not voter:
            self.respond('ERROR', 'You\'re not logged in!')
            return
        
        # Get the election from the database
        election_id = formData['election_id']
        election = db.get(election_id)
        if not election:
            self.respond('ERROR', 'Invalid election!')
        
        # Make sure user is eligible to vote
        status = database.voter_status(voter, election)
        if status == 'voted':
            self.respond('ERROR', 'You have already voted for this election.')
            return
        elif status == 'not_eligible':
            self.respond('ERROR', 'You are not eligible to vote for this election.')
            return
        elif status == 'invalid_time':
            self.respond('ERROR', 'You are not in the eligible voting time for this election.')
            return
        if status != 'eligible':
            self.respond('ERROR', 'You are not eligible to vote for this election.')
            return
        
        database.mark_voted(voter, election)
        
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