import database
import irv
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
            
            # Only Ranked Choice currently supported
            if election_position.type == 'Ranked-Choice':
                self.ranked_choice_results(election_position)
            else:
                logging.info('Results for %s position type not supported', election_position.type)
                continue
            
        election.result_computed = True
        election.put()
    
    @staticmethod
    def ranked_choice_results(election_position):
        """
        Computes winner results for ranked choice position and updates the winners.
        
        Args:
            election_position {ElectionPosition}: the ranked choice election position.
        """
        assert election_position.type == 'Ranked-Choice'
        ballots = []
        for ballot in election_position.ranked_ballots:
            ballots.append(ballot.preferences)
        
        winners = irv.run_irv(ballots, election_position.slots)
        for winner in winners:
            winner_candidate = database.ElectionPositionCandidate.get(winner)
            winner_candidate.winner = True
            winner_candidate.put()
        
            
app = webapp2.WSGIApplication([
        ('/compute-results', ComputeResultsHandler)
], debug=True)