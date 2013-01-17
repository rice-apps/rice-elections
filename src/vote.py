"""
Back-end for the vote page.
"""

__authors__ = ['Waseem Ahmad (waseem@rice.edu)', 'Andrew Capshaw (capshaw@rice.edu)']

import authentication
import database
import datetime
import logging
import webapp2

from authentication import require_login
from main import render_page

class VoteHandler(webapp2.RequestHandler):
    """
    Handles GET requests for the Vote page.
    """

    def get(self):
        page_data = {'open_elections': [], 'election_results': []}

        # Authenticate user
        voter = authentication.get_voter()
        if not voter:
            require_login(self)
        
        # Elections the user is eligible to vote for
        elections = voter.elections
        logging.info(elections)

        for election in elections:
            logging.info('Found election')
            data = {}
            data['id'] = str(election.key())
            data['name'] = election.name
            now = datetime.datetime.now()
            if now > election.end:      # Election passed
                data['end_date'] = election.end.strftime('%a, %B %d, %Y, %I:%M %p') + ' UTC'
                page_data['election_results'].append(data)
            else:
                data['user_action'] = 'not_started' # Initial assumption
                
                # Check election times
                if election.start > now:
                    start_str = election.start.strftime('%a, %B %d, %Y, %I:%M %p') + ' UTC'
                    data['status'] = {'text': 'Voting begins on', 'date': start_str}
                    data['user_action'] = 'not_started'
                else:
                    end_str = election.end.strftime('%a, %B %d, %Y, %I:%M %p') + ' UTC'
                    data['status'] = {'text': 'Voting ends on', 'date': end_str}
                    data['user_action'] = 'vote'
                    
                # Check to see if the user has already voted
                if database.voter_status(voter, election) == 'voted':
                    data['user_action'] = 'voted'
                
                page_data['open_elections'].append(data)
            logging.info(data)

        render_page(self, '/vote', page_data)


app = webapp2.WSGIApplication([
        ('/vote', VoteHandler)
], debug=True)