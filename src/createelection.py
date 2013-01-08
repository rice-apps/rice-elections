"""
Back-end for the Create Election Form.
"""

__author__ = 'Waseem Ahmad (waseem@rice.edu)'

import database
import json
import logging
import webapp2

TEST_DATA = {u'start': 1358898900,
             u'end': 1359071700,
             u'organization': 'Brown College',
             u'name': u'Round 1',
             u'voters': [u'wa1', u'sa27', u'nfa11', u'srt6'],
             u'positions': [
                    {u'candidates': [u'Candidate A', u'Candidate B'], u'slots': 1, u'writeIn': True, u'type': u'Ranked-Choice', u'name': u'President'}, 
                    {u'candidates': [u'Candidate 1', u'Candidate 2'], u'slots': 1, u'writeIn': False, u'type': u'Ranked-Choice', u'name': u'Chief Justice'}
             ]}

class CreateElectionHandler(webapp2.RequestHandler):
    """
    Handles POST submissions from the Create Election Form.
    """
    
    def post(self):
        logging.info('Received new create election submission')
        logging.info(self.request.POST)
        
        formData = self.request.get('formData')
        if not formData:
            self.response.out.write('No Form Data Sent!')
            return
        
        electionData = json.loads(formData)
        organization = database.get_organization('Brown College')
        if not organization:
            logging.info('Organization not found')
            return
        
        election = database.put_election(electionData['name'], electionData['start'],
                                         electionData['end'], organization)
        database.add_eligible_voters(election, electionData['voters'])
        logging.info(electionData)
        
        self.response.out.write('Election successfully created!')
        
        
app = webapp2.WSGIApplication([
        ('/createElection', CreateElectionHandler)
], debug=True)