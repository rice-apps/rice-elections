"""
Back-end for the vote page.
"""

__authors__ = ['Waseem Ahmad (waseem@rice.edu)', 'Andrew Capshaw (capshaw@rice.edu)']

import logging
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
        
        render_page(self, '/vote', page_data)


app = webapp2.WSGIApplication([
        ('/vote', VoteHandler)
], debug=True)