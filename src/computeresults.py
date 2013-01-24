import database
import logging
import webapp2

from datetime import datetime
from google.appengine.ext import db

class ComputeResultsHandler(webapp2.RequestHandler):
    def get(self):
        """
        Computes election results and stores them in the database if they have ended.
        """
        election = database.Election.gql('WHERE result_computed=FALSE AND end<:1', datetime.now()).get()
        if not election:
            return
        
        logging.info('Computing results for election: %s, organization: %s.', election.name, election.organization.name)
        for election_position in election.election_positions:
            logging.info('Computing election position: %s', election_position.position.name)
            election_position.compute_winners()
            
        election.result_computed = True
        election.put()
        
            
app = webapp2.WSGIApplication([
        ('/compute-results', ComputeResultsHandler)
], debug=True)