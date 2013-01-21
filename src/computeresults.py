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
            
            # Only Ranked Choice currently supported
            if election_position.type == 'Ranked-Choice':
                self.ranked_choice_results(election_position)
            else:
                logging.info('Results for %s position type not supported', election_position.type)
                continue
    
    @staticmethod
    def ranked_choice_results(election_position):
        """
        Computes winner results for ranked choice position and updates the winners.
        
        Args:
            election_position {ElectionPosition}: the ranked choice election position.
        """
        assert election_position.type == 'Ranked-Choice'
        candidates = []
        for epc in election_position.election_position_candidates:
            epc_id = str(epc.key())
            epc_name = epc.candidate.name
            votes = {}
            for rv in epc.ranked_votes:
                rank = rv.rank
                if rank not in votes:
                    votes[rank] = 1
                else:
                    votes[rank] += 1
            candidates.append({'id': epc_id,
                               'name': epc_name,
                               'votes': votes})
        
        logging.info(candidates)
            
app = webapp2.WSGIApplication([
        ('/compute-results', ComputeResultsHandler)
], debug=True)