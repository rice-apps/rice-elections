"""
Back-end for the Create Election Form.
"""

__author__ = 'Waseem Ahmad (waseem@rice.edu)'

import database
import json
import logging
import webapp2

from google.appengine.ext import db

TEST_DATA = {u'start': 1357659600, 
             u'positions': [
                {u'candidates': [{u'name': u'Waseem Ahmad', u'netId': u'wa1'}, 
                                 {u'name': u'Sal Testa', u'netId': u'srt6'}], 
                     u'slots': 1, 
                     u'writeIn': False, 
                     u'type': u'Ranked-Choice', 
                     u'name': u'President'}, 
                {u'candidates': [{u'name': u'Sal Testa', u'netId': u'srt6'}, 
                                 {u'name': u'Andrew Capshaw', u'netId': u'apc3'}],
                 u'slots': 1,
                 u'writeIn': True,
                 u'type': u'Ranked-Choice',
                 u'name': u'Chief Justice'}],
             u'end': 1357832100,
             u'name': u'Round One',
             u'voters': [u'wa1', u'srt6', u'apc3']}


class CreateElectionHandler(webapp2.RequestHandler):
    """
    Handles POST submissions from the Create Election Form.
    """
    
    def post(self):
        logging.info('Received new create election submission')
        logging.info(self.request.POST)
        
        try:
            # Get form data
            formData = self.request.get('formData')
            if not formData:
                msg = 'No Form Data Sent!'
                self.respond('ERROR', msg)
                logging.error(msg)
                return
            
            # Parse form data
            electionData = json.loads(formData)

            # Get organization
            organization = database.get_organization('Brown College')
            if not organization:
                msg = 'Organization not found!'
                self.respond('ERROR', msg)
                logging.error(msg)
                return
            
            # Store election
            election = database.put_election(electionData['name'], electionData['start'],
                                             electionData['end'], organization)
            database.add_eligible_voters(election, electionData['voters'])
            
            # Store positions
            for position in electionData['positions']:
                position_name = position['name']
                position_entry = database.get_position(position_name, organization, create=True)
                election_position_entry = database.put_election_position(
                                                election,
                                                position_entry,
                                                position['slots'],
                                                position['write_in'],
                                                position['type'],
                                                position['vote_required'])
                
                # Store candidates
                for candidate in position['candidates']:
                    candidate_entry = database.get_candidate(candidate['name'], candidate['netId'], create=True)
                    database.put_candidate_for_election_position(candidate_entry, election_position_entry)
            
                for candidate in election_position_entry.candidates:
                    candidate_entry = db.get(candidate)
                    logging.info('Candidate %s running for %s', candidate_entry.name, 
                                 election_position_entry.position.name)
            
            logging.info(electionData)
        except Exception as e:
            msg = 'Sorry! An error occurred: %s' % str(e)
            logging.error(msg)
            self.respond('ERROR', msg)
            
        
        # Success
        msg = 'Election successfully created!'
        self.respond('OK', msg)
        logging.info(msg)

    def respond(self, status, message):
        """
        Sends a response to the front-end.
        
        Args:
            status: response status
            message: response message
        """
        self.response.write(json.dumps({'status': status, 'msg': message}))
        
app = webapp2.WSGIApplication([
        ('/create-election', CreateElectionHandler)
], debug=True)