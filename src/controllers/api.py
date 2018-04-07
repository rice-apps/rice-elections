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

    def get(self):
        # orgs = [org.to_dict() for org in models.Organization.all()]
        # random.shuffle(orgs)
        # logging.info(orgs)

        election = models.Election.gql('').fetch(1)[0].to_json()
        logging.info(election)

        self.response.write(json.dumps({'election': election}))

app = webapp2.WSGIApplication([
    ('/api/organizations', OrganizationHandler)
], debug=True)
