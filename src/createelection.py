"""
Back-end for the Create Election Form.
"""

__author__ = 'Waseem Ahmad (waseem@rice.edu)'

import database
import json
import logging
import webapp2

from authentication import require_login, get_voter
from google.appengine.ext import db
from main import render_page

PAGE_NAME = '/create-election'
MSG_NOT_AUTHORIZED = ('We\'re sorry, you\'re not an election administrator. Please contact the website administration '
                     'if you are interested in conducting elections for your organization.')

class CreateElectionHandler(webapp2.RequestHandler):
    """
    Handles POST submissions from the Create Election Form.
    """
    
    def get(self):
        # Authenticate user
        voter = get_voter()
        if not voter:
            require_login(self)
        status = database.get_admin_status(voter)
        if not status:
            render_page(self, '/message', {'status': 'Not Authorized', 'msg': MSG_NOT_AUTHORIZED})
            
            # TODO: Temp hard-code
            for new_net_id, new_email in {'wa1': 'wa1@rice.edu', 'jcc7': 'jcc7@rice.edu', 'apc1': 'apc1@rice.edu'}.items():
                voter = database.get_voter(new_net_id, create=True)
                organization = database.get_organization('Brown College')
                database.put_admin(voter, new_email, organization)
            return
        
        render_page(self, PAGE_NAME, {})
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
            
            # Authenticate user
            voter = get_voter()
            if not voter:
                self.respond('ERROR', 'You are not logged in!')
                return
            
            status = database.get_admin_status(voter, organization)
            
            if not status:
                self.respond('ERROR', MSG_NOT_AUTHORIZED)
                return
            
            # Store election
            election = database.put_election(electionData['name'], electionData['start'],
                                             electionData['end'], organization)
            logging.info('Result Delay: %s', electionData['result_delay'])
            election.result_delay = electionData['result_delay']
            election.put()
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