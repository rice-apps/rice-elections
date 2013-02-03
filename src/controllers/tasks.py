"""
Controller for tasks related requests.
"""

import webapp2

from models.tasks import ElectionVoterFactory, ElectionResultsFactory

app = webapp2.WSGIApplication([
    ('/tasks/election-voter-factory', ElectionVoterFactory),
	('/tasks/election-results-factory', ElectionResultsFactory)
], debug=True)