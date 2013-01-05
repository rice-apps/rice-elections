"""
Back-end for the Create Election Form.
"""

__author__ = 'Waseem Ahmad (waseem@rice.edu)'

import database
import json
import logging
import webapp2

from google.appengine.ext import db

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
        organization = self.getOrganization(electionData)
        if not organization:
            logging.info('Organization not found')
        logging.info(electionData)
        
    def getOrganization(self, electionData):
        """
        Returns the organization the election data is referring to.
        
        Args:
            electionData: A dictionary with election data.
        
        Returns:
            Organization from database. None if it doesn't exist.
        """
        # Temporary hard coding
        # TODO: Verify the election admin is authorized to create an election
        # for the specified organization
        electionData['organization'] = 'Brown College'
        
        organization_name = electionData.get('organization')
        if not organization_name:
            return None
        
        query_result = db.GqlQuery('SELECT * FROM Organization WHERE name="%s" LIMIT=1' % organization_name).run()
        organization = query_result.next()
        return organization
        
app = webapp2.WSGIApplication([
        ('/createElection', CreateElectionHandler)
], debug=True)