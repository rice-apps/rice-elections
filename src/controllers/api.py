import json
import random

import logging
import webapp2

from models import models
from models import webapputils

__author__ = 'Savion Lee <harmonica1243@gmail.com>'

###
# This is a controller to server up data to the Angular2 frontend of the site.
###

class OrganizationHandler(webapp2.RequestHandler):
    """Handles GET requests for static pages."""


    # sample id: ag1kZXZ-b3dsZWN0aW9ucg8LEghFbGVjdGlvbhiPAgw
    def get(self):
        # orgs = [org.to_dict() for org in models.Organization.all()]
        # random.shuffle(orgs)
        # logging.info(orgs)

        id = self.request.get("id")
        #  sample id = "ag1kZXZ-b3dsZWN0aW9ucg8LEghFbGVjdGlvbhiPAgw"


        election = models.Election.get(id).to_json()
        logging.info(election)
        logging.info("hellloooooooooooo")
        self.response.write(json.dumps({"election": election}))


        # old code:
        # election = models.Election.gql('').fetch(1)[0].to_json()
        #self.response.write(json.dumps({"election": {"name":"the id: "+id}}))


    # after successfully getting, will need to write another method called update

app = webapp2.WSGIApplication([
    ('/api/organizations', OrganizationHandler),
], debug=True)

# This didn't work: adding this tuple to the list of routes
# webapp2.Route('/api/organizations/<id:\d+>', handler="OrganizationHandler:get_by_id", name = "election-by-id", handler_method='get_by_id')

# This is helpful: http://webapp2.readthedocs.io/en/latest/guide/routing.html