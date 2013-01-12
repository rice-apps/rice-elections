"""
Back-end for the vote page.
"""

__authors__ = ['Waseem Ahmad (waseem@rice.edu)', 'Andrew Capshaw (capshaw@rice.edu)']

import datetime
import database
import logging
import random
import webapp2

from main import render_page, require_login

class VoteHandler(webapp2.RequestHandler):
    """
    Handles GET requests for the Vote page.
    """

    def get(self):
        page_data = {'open_elections': [], 'election_results': []}

        # Authenticate user
        net_id = require_login(self)
        voter = database.get_voter(net_id)
        if not voter:
            render_page(self, '/vote', page_data)
            return
        
        # Elections the user is eligible to vote for
        elections = voter.elections
        logging.info(elections)

        for election in elections:
            logging.info('Found election')
            data = {}
            data['name'] = election.name
            now = datetime.datetime.now()
            if now > election.end:
                data['end_date'] = election.end.strftime("%a, %B %d, %Y")
                page_data['election_results'].append(data)
            else:
                data['user_voted'] = True if random.random() > 0.5 else False   # LOL
                if election.start > now:
                    start_str = election.start.strftime('%a, %B %d, %Y, %I:%M %p')
                    data['status'] = 'Voting begins at %s' % start_str
                else:
                    end_str = election.end.strftime('%a, %B %d, %Y, %I:%M %p')
                    data['status'] = 'Voting ends at %s' % end_str
                page_data['open_elections'].append(data)

        render_page(self, '/vote', page_data)


app = webapp2.WSGIApplication([
        ('/vote', VoteHandler)
], debug=True)