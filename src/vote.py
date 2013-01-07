"""
Back-end for the vote page.
"""

__authors__ = ['Waseem Ahmad (waseem@rice.edu)', 'Andrew Capshaw (capshaw@rice.edu)']

import datetime
import database
import logging
import random
import webapp2

from main import render_page

class VoteHandler(webapp2.RequestHandler):
    """
    Handles GET requests for the Vote page.
    """
    
    def get(self):
        page_data = {'open_elections': [{'name' : 'Brown College Spring Elections First Round',
                                             'status': 'Voting ends in 1 day 23 hours 51 minutes',
                                             'user_voted': False},
                                            {'name' : 'Rice CS Club Officers',
                                             'status': 'Voting begins in 3 days 12 hours 14 minutes',
                                             'user_voted': True}],
                         'election_results': [{'name' : 'Brown College Spring Elections First Round',
                                               'end_date': 'Mon January 21, 2013 11:55 PM'},
                                              {'name' : 'Rice CS Club Officers',
                                               'end_date': 'Mon January 21, 2013 11:55 PM'}]}
        voter = database.get_voter('wa1')
        if not voter:
            render_page(self, '/vote', page_data)
            return
        
        elections = voter.get_elections().run()
        logging.info(elections)
        page_data = {'open_elections': [], 'election_results': []}
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
                    data['status'] = 'Voting ends at %s', end_str
                page_data['open_elections'].append(data)
        
        render_page(self, '/vote', page_data)


app = webapp2.WSGIApplication([
        ('/vote', VoteHandler)
], debug=True)