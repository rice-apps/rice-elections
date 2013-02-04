"""
Controller for voting related requests.
"""

import webapp2

from models.vote import VoteHandler
from models.vote_.cast_ballot import BallotHandler
from models.vote_.view_results import ResultsHandler

app = webapp2.WSGIApplication([
    ('/vote', VoteHandler),
    ('/vote/cast-ballot', BallotHandler),
    ('/vote/view-results', ResultsHandler)
], debug=True)