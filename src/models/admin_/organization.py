"""
Back-end for the Organization Panel.
"""

__author__ = 'Waseem Ahmad <waseem@rice.edu>'

import json
import logging
import webapp2

from authentication import auth
from datetime import datetime, timedelta
from google.appengine.api import taskqueue
from google.appengine.ext import db
from models import models, webapputils

PAGE_NAME = '/admin/organization'
MSG_NOT_AUTHORIZED = ('We\'re sorry, you\'re not an organization administrator. Please contact the website administration '
                     'if you are interested in conducting elections for your organization.')

class OrganizationPanelHandler(webapp2.RequestHandler):

    def get(self):
        # Authenticate user
        voter = auth.get_voter(self)
        status = models.get_admin_status(voter)
        if not status:
            logging.info('Not authorized')
            webapputils.render_page(self, '/templates/message',
                {'status': 'Not Authorized', 'msg': MSG_NOT_AUTHORIZED})
            return

        # Get organization information
        admin = models.Admin.gql('WHERE voter=:1', voter).get()
        logging.info("<Admin: %s>", admin.email)
        # TODO: This should be fetch to get the list of organizations.
        org_admin = models.OrganizationAdmin.gql('WHERE admin=:1',
                                                    admin).get()
        logging.info("<Admin of Organizations: %s>", org_admin.organization.name)
        if not org_admin:
            logging.info('Not authorized')
            webapputils.render_page(self, '/templates/message',
                {'status': 'Not Authorized', 'msg': MSG_NOT_AUTHORIZED})
            return
        org = org_admin.organization
        # TODO(adam): This should be removed. Instead, the admin section of the entire website 
        # should pull up all the organizations the logged-in user is an admin of and provide 
        # a selection for which organization the admin wants to manage (need some html change).
        # I am thinking about a drop down menu that includes all the organizations in page rendering. 
        # Then that organization should be referred by its unique id in the url of the admin panel.
        auth.set_organization(org)

        # Construct page information
        # TODO(adam): The way the page is rendered should be changed to accomodate the
        # organization list.
        page_data = {}
        page_data['organization'] = org
        page_data['admins'] = self.admin_list(org)
        page_data['elections'] = [elec.to_json(True) for elec in org.elections]
        logging.info(page_data['elections'])
        logging.info(page_data)
        # TODO(adam): webapputils need change to render the page in a new way.
        webapputils.render_page(self, PAGE_NAME, page_data)

    def post(self):
        # Authenticate user
        voter = auth.get_voter()
        if not voter:
            self.respond('ERROR', MSG_NOT_AUTHORIZED)
            return
        status = models.get_admin_status(voter)
        if not status:
            self.respond('ERROR', MSG_NOT_AUTHORIZED)
            return

        # Get method and data
        logging.info('Received call')
        data = json.loads(self.request.get('data'))
        methods = {'update_profile': self.update_profile}
        methods[data['method']](data['data'])

    def respond(self, status, message):
        """
        Sends a response to the front-end.

        Args:
            status: response status
            message: response message
        """
        self.response.write(json.dumps({'status': status, 'msg': message}))

    def update_profile(self, data):
        """
        Updates the organization profile.
        """
        logging.info('Updating profile')
        org_id = data['id']
        org = models.Organization.get(org_id)
        assert models.get_admin_status(auth.get_voter(), org)
        for field in ['name', 'description', 'website']:
            setattr(org, field, data[field].strip())
        org.put()
        self.respond('OK', 'Updated')

    @staticmethod
    def admin_list(organization):
        admins = []
        for organization_admin in organization.organization_admins:
            admin = {}
            admin['name'] = organization_admin.admin.name
            admin['email'] = organization_admin.admin.email
            admins.append(admin)
        return admins
