"""
Controller to handle api calls for json data.
"""

import datetime
import json
import logging
import sys
import webapp2

from authentication import auth
from models import models, webapputils, report_results
from google.appengine.api import mail, taskqueue

COMMANDERS = ['stl2']


class CommandCenterAPI(webapp2.RequestHandler):
    def get(self):
            voter = auth.get_voter(self)
            if voter.net_id not in COMMANDERS:
                return webapputils.render_page(self, '/templates/message', {
                    'status': 'Not Authorized',
                    'msg': "You're not authorized to enter the command center"
                })

            organizations = []
            # Aggregate all information about organizations
            for org in models.Organization.all():
                organizations.append({
                    'name': org.name,
                    'electionCount': org.elections.count(),
                    'adminCount': org.organization_admins.count(),
                    'voteCount': sum([elec.voted_count for elec in org.elections])
                })


            # get 20 elections that have not ended, sorted by starting time
            elections = [e.to_json(True) for e in
                models.Election.all().order('-end').order('start').run(limit=20)]
            page_data = {
                "organizations": organizations,
                "elections": elections
            }
            self.response.headers['Content-Type'] = 'application/json'
            self.response.write(json.dumps(page_data))

app = webapp2.WSGIApplication([
    ('/api/command-center', CommandCenterAPI)
], debug=True)