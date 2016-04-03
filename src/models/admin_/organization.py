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
        org_admin = models.OrganizationAdmin.gql('WHERE admin=:1',
                                                    admin).fetch(None)
        logging.info("<Admin of Organizations: %s>", [oa.organization.name for oa in org_admin])
        if not org_admin:
            logging.info('Not authorized')
            webapputils.render_page(self, '/templates/message',
                {'status': 'Not Authorized', 'msg': MSG_NOT_AUTHORIZED})
            return
        orgs = [org_admin.organization for org_admin in org_admin]
        auth.set_organizations(orgs)

        # Pick one organization to display information about.
        org_param = self.request.get('org')

        if org_param:   # Wants to change current active organization
            org_req = models.Organization.get(org_param)
            auth.set_active_organization(org_req)

        elif auth.get_active_organization():    # Did not intend a change in the active organization
            pass

        else:   # No active organizations have been set yet
            auth.set_active_organization(orgs[0])

        # Construct page information
        page_data = {}
        page_data['organizations'] = orgs
        page_data['active_org'] = auth.get_active_organization()
        page_data['admins'] = self.admin_list(auth.get_active_organization())
        page_data['elections'] = [elec.to_json(True) for elec in auth.get_active_organization().elections]
        logging.info(page_data['elections'])
        logging.info(page_data)
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
