"""
Controller for website administration stuff.
"""

import json
import webapp2

from authentication import auth
from models import models, webapputils

COMMANDERS = ['wa1', 'sa27', 'jcc7']

class CommandCenterHandler(webapp2.RequestHandler):

    def get(self):
        voter = auth.get_voter(self)
        if voter.net_id not in COMMANDERS:
            return self.render_template('/templates/message', {
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

        page_data = {
            "organizations": organizations
        }

        return webapputils.render_page(self, '/intern/command-center', page_data)

    def post(self):
        methods = {
            'create_organization': self.create_organization,
            'add_admin': self.add_admin
        }
        data = json.loads(self.request.get('data'))
        voter = auth.get_voter(self)
        if voter.net_id not in COMMANDERS:
            return  # hacker
        out = methods[data['method']](data)

    def create_organization(self, data):
        org = models.Organization(
            name=data['name'],
            description=data['description'],
            website=data['website']
        )
        org.put()
        webapputils.respond(self, 'OK', 'Done')

    def add_admin(self, data):
        org = models.Organization.get(data['organization'])
        voter = get_voter(data['net_id'], create=True)
        org_admin = models.put_admin(voter, data['email'], org)
        if org_admin:
            webapputils.respond(self, 'OK', 'Done')
        else:
            webapputils.respond(self, 'ERROR', "Couldn't create admin")


app = webapp2.WSGIApplication([
    ('/intern/command-center', CommandCenterHandler)
], debug=True)
