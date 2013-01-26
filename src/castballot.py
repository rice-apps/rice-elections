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
REF_DATA = {u'positions': [
                {u'skipped': False, 
                 u'name': u'President', 
                 u'required': True, 
                 u'candidate_rankings': [
                        {u'name': u'Candidate B', 
                         u'rank': 1, 
                         u'id': u'ag5kZXZ-b3dsZWN0aW9uc3IPCxIJQ2FuZGlkYXRlGBQM'}, 
                        {u'name': u'Candidate A', 
                         u'rank': 2, 
                         u'id': u'ag5kZXZ-b3dsZWN0aW9uc3IPCxIJQ2FuZGlkYXRlGBMM'}], 
                 u'type': u'Ranked-Choice', 
                 u'id': u'ag5kZXZ-b3dsZWN0aW9uc3IWCxIQRWxlY3Rpb25Qb3NpdGlvbhgSDA'}, 
                {u'skipped': True, 
                 u'name': u'Chief Justice', 
                 u'required': False, 
                 u'candidate_rankings': [
                        {u'name': u'Candidate A', 
                         u'rank': u'', 
                         u'id': u'ag5kZXZ-b3dsZWN0aW9uc3IPCxIJQ2FuZGlkYXRlGBcM'}, 
                        {u'name': u'Candidate B', 
                         u'rank': u'', 
                         u'id': u'ag5kZXZ-b3dsZWN0aW9uc3IPCxIJQ2FuZGlkYXRlGBQM'}], 
                 u'type': u'Ranked-Choice', 
                 u'id': u'ag5kZXZ-b3dsZWN0aW9uc3IWCxIQRWxlY3Rpb25Qb3NpdGlvbhgWDA'}], 
            u'election_id': u'ag5kZXZ-b3dsZWN0aW9uc3IOCxIIRWxlY3Rpb24YCww'}

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
        for key, value in election.to_json().items():
            page_data[key] = value
        page_data['positions'] = []
        page_data['voter_net_id'] = voter.net_id

        # Write position information
        election_positions = election.election_positions
        for election_position in election_positions:
            position = {}
            for key, value in election_position.to_json().items():
                position[key] = value
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
        
        # Verify that the user has voted correctly
        verified_positions = {}           # Whether an election_position has been verified
        for election_position in election.election_positions:
            verified_positions[str(election_position.key())] = False
        
        for position in formData['positions']:
            if position['type'] == 'Ranked-Choice':
                verified_positions[position['id']] = self.verify_ranked_choice_ballot(position)
            elif position['type'] == 'Cumulative-Voting':
                verified_positions[position['id']] = self.verify_cumulative_voting_ballot(position)
            else:
                logging.error('Encountered unknown position type: %s', position['type'])
                verified_positions[position['id']] = False
        
        logging.info('Verified Positions: %s', verified_positions)
        for verified in verified_positions.values():
            if verified == False:
                self.respond('ERROR', 'You have attempted to cast an invalid ballot. Please verify that you are following all instructions.')
                return
        
        # Record all of the votes
        for position in formData['positions']:
            if verified_positions[position['id']]:
                if position['type'] == 'Ranked-Choice':
                    self.cast_ranked_choice_ballot(position)
            
#        database.mark_voted(voter, election)
        
        self.respond('OK', 'Your ballot has been successfully cast!')
        
    def respond(self, status, message):
        """
        Sends a response to the front-end.
        
        Args:
            status: response status
            message: response message
        """
        self.response.write(json.dumps({'status': status, 'msg': message}))
    
    @staticmethod
    def verify_ranked_choice_ballot(position):
        """
        Verifies the validity a ranked choice ballot.
        
        Args:
            position{dictionary}: the position dictionary from the client
        
        Returns:
            True if valid, False if invalid. None if empty ballot.
        """
        logging.info('Verifying ranked choice ballot.')
        election_position = database.RankedVotingPosition.get(position['id'])
        if not election_position:
            logging.info('No election position found in database.')
            return False
        assert election_position.type == 'Ranked-Choice'
        
        required = election_position.vote_required
        election_position_candidates = database.ElectionPositionCandidate.gql('WHERE election_position=:1 AND written_in=False',
                                                                    election_position)
        num_ranks_required = election_position_candidates.count()
        write_in = election_position.write_in
        ranks = []
        candidates_verified = {}
        for election_position_candidate in election_position_candidates:
            candidates_verified[str(election_position_candidate.key())] = False
        for candidate_ranking in position['candidate_rankings']:
            if not candidate_ranking['rank']:
                if required: 
                    logging.info('Ranking required but not provided')
                    return False   # Ranking required but not provided
                else: return None           # Empty ballot
            else:
                ranks.append(candidate_ranking['rank'])
                candidates_verified[candidate_ranking['id']] = True
                if candidate_ranking['id'] == 'write-in':
                    if not write_in:
                        logging.info('Write-in not allowed.')
                        return False        # Write in not allowed
                    elif candidate_ranking['rank']:
                        num_ranks_required += 1
                    else:
                        logging.info('Write in was specified but not ranked')
                        return False        # Write in was specified but not ranked
                    
        for verified in candidates_verified.values():
            if not verified: 
                logging.info('Not all candidates verified')
                return False   # Not all candidates verified
        ranks.sort()
        if len(ranks) == 0 and not required: return True
        if ranks[0] != 1 or ranks[len(ranks)-1] != num_ranks_required: return False    # Number of rankings don't match
        if num_ranks_required > election_position.write_in_slots: return False
        logging.info('Ballot for position %s verified.', election_position.position.name)
        return True

    @staticmethod
    def cast_ranked_choice_ballot(position):
        """
        Records a ranked choice ballot in the database. Modifies write-in ids of the dictionary to reflect the 
        written-in candidate's id.
        
        Args:
            position{dictionary}: the verifies position dictionary from the client
        """
        election_position = database.ElectionPosition.get(position['id'])
        preferences = [None] * len(position['candidate_rankings'])
        for cr in position['candidate_rankings']:
            
            # Check for a write-in
            if cr['id'] == 'write-in':
                epc = database.ElectionPositionCandidate.gql('WHERE election_position=:1 AND name=:2',
                                                             election_position, cr['name']).get()
                if not epc:
                    epc = database.ElectionPositionCandidate(election_position=election_position,
                                                             net_id=None,
                                                             name=cr['name'],
                                                             written_in=True)
                    epc.put()
                cr['id'] = str(epc.key())
            rank = cr['rank']
            preferences[rank-1] = database.ElectionPositionCandidate.get(cr['id']).key()
        
        logging.info(preferences)
        assert None not in preferences
        ballot = database.RankedBallot(election_position=election_position,
                                       preferences=preferences)
        ballot.put()
        logging.info('Stored ballot in database with preferences %s', preferences)

    def verify_cumulative_voting_ballot(position):
        """
        Verifies the validity a cumulative voting ballot.
        
        Args:
            position{dictionary}: the position dictionary from the client
        
        Returns:
            True if valid, False if invalid. None if empty ballot.
        """
        logging.info('Verifying cumulative choice ballot.')
        election_position = database.CumulativeVotingPosition.get(
            position['id'])
        if not election_position:
            logging.info('No election position found in database.')
            return False
        assert election_position.type == 'Cumulative-Voting'

        required = election_position.vote_required
        election_position_candidates = database.ElectionPositionCandidate.gql(
            'WHERE election_position=:1 AND written_in=False',
            election_position)
        points_required = election_position.points
        points_used = 0
        for epc in election_position_candidates:
            candidates_verified[str(epc.key())] = False
        for cp in position['candidate_points']:
            points_used += cp['points']
            


                
app = webapp2.WSGIApplication([
        ('/cast-ballot', BallotHandler)
], debug=True)