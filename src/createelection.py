"""
Back-end for the Create Election Form.
"""

__author__ = 'Waseem Ahmad <waseem@rice.edu>'

import database
import json
import logging
import webapp2

from authentication import require_login, get_voter
from datetime import datetime, timedelta
from google.appengine.api import taskqueue
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
            if voter.net_id != 'wa1':
                return
            # TODO: Temp hard-code
            for new_net_id, new_email in {'wa1': 'wa1@rice.edu', 'jcc7': 'jcc7@rice.edu', 'apc1': 'apc1@rice.edu'}.items():
                voter = database.get_voter(new_net_id, create=True)
                organization = database.get_organization('Brown College')
                database.put_admin(voter, new_email, organization)
            return
        
        render_page(self, PAGE_NAME, {})
    def post(self):
        logging.info('Received new create election submission')
        
        try:
            # Get form data
            formData = self.request.get('formData')
            logging.info(formData)
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
            election = database.Election(
                name=electionData['name'],
                start=datetime.fromtimestamp(electionData['start']),
                end=datetime.fromtimestamp(electionData['end']),
                organization=organization,
                universal=electionData['universal'],
                result_delay=electionData['result_delay'])
            election.put()
            if not election.universal:
                election_key = str(election.key())
                voter_list = electionData['voters']
                data = {'election_key': election_key,
                        'voter_list': voter_list}
                retry_options = taskqueue.TaskRetryOptions(task_retry_limit=0)
                taskqueue.add(url='/tasks/election-voter-factory',
                              params={'data':json.dumps(data)},
                              retry_options=retry_options)
            
            # Store positions
            for position in electionData['positions']:
                position_name = position['name']
                position_entry = database.get_position(position_name,
                                                       organization,
                                                       create=True)
                if position['type'] == 'Ranked-Choice':
                    ep = database.RankedVotingPosition(
                        election=election,
                        position=position_entry,
                        vote_required=position['vote_required'],
                        write_in_slots=position['write_in'])
                    ep.put()
                elif position['type'] == 'Cumulative-Voting':
                    ep = database.CumulativeVotingPosition(
                        election=election,
                        position=position_entry,
                        vote_required=position['vote_required'],
                        write_in_slots=position['write_in'],
                        points=position['points'],
                        slots=position['slots'])
                    ep.put()
                else:
                    raise Exception('Unknown position type')

                # Store candidates
                for candidate in position['candidates']:
                    database.ElectionPositionCandidate(
                        election_position=ep,
                        net_id=candidate['netId'],
                        name=candidate['name']).put()
                    logging.info('%s running for %s', candidate['name'], ep.position.name)
                
            # Enqueue task for computing results after election ends
            compute_time = election.end + timedelta(seconds=5)
            data = {'election_key': str(election.key())}
            retry_options = taskqueue.TaskRetryOptions(task_retry_limit=0)
            taskqueue.add(url='/tasks/election-results-factory',
                          params={'data': json.dumps(data)},
                          eta=compute_time,
                          retry_options=retry_options)
            logging.info('Election result computation enqueued.')
            logging.info(electionData)
        except NameError as e:
            msg = 'Sorry! An error occurred: %s' % str(e)
            logging.error(msg)
            self.respond('ERROR', msg)
            return
            
        
        # Success
        msg = ('Election successfully created! Adding the eligible voters '
               'requires some additional processing that should be completed '
               'soon. You will receive a confirmation email once the task is '
               'complete.')
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