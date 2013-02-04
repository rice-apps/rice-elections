"""
Back-end for the Election Panel.
"""

__author__ = 'Waseem Ahmad <waseem@rice.edu>'

import models
import json
import logging
import webapp2

from authentication import require_login, get_voter
from datetime import datetime, timedelta
from google.appengine.api import taskqueue
from google.appengine.ext import db
from main import render_html, render_page, render_page_content, get_page, JINJA_ENV

PAGE_NAME = '/admin/organization-panel/election-panel'
MSG_NOT_AUTHORIZED = ('We\'re sorry, you\'re not an organization administrator. Please contact the website administration '
                     'if you are interested in conducting elections for your organization.')
PANEL_BAR = [
    {'text': 'Election Information', 'link': PAGE_NAME+'/information'},
    {'text': 'Positions', 'link': PAGE_NAME+'/positions'},
    {'text': 'Voters', 'link': PAGE_NAME+'/voters'}]


class ElectionPanelHandler(webapp2.RequestHandler):
    
    def get(self):
        # Authenticate user
        voter = get_voter()
        if not voter:
            require_login(self)
        status = models.get_admin_status(voter)
        if not status:
            render_page(self, '/message', {'status': 'Not Authorized', 'msg': MSG_NOT_AUTHORIZED})
            return

        # Get organization information
        admin = models.Admin.gql('WHERE voter=:1', voter).get()
        org_admin = models.OrganizationAdmin.gql('WHERE admin=:1',
                                                    admin).get()
        org = org_admin.organization

        # Construct page information
        page_data = {}
        page_data['id'] = self.request.get('id')
        panel = get_panel(self.request.path + '/information', page_data, page_data['id'])
        logging.info(panel)
        render_page_content(self, PAGE_NAME, panel)

    def post(self):
        data = json.loads(self.request.get('data'))
        method = data['method']
        election_id = data['id']
        election = {}
        if election_id:
            election_entry = models.Election.get(election_id)
            election = election_entry.to_json()
        render_html(self, '/election-panel-information', election)
        return None


def get_panel(page_name, page_data, election_id):
    logging.info(page_name)
    panel_content = get_page(page_name, page_data)
    logging.info(panel_content)
    # Mark all links in the panel bar as inactive except the page open
    for item in PANEL_BAR:
        item['active'] = (item['link'] == page_name)

    panel = JINJA_ENV.get_template(
        'admin/organization-panel/election-panel.html')
    panel_vals = {'id': election_id,
                  'panel_bar': PANEL_BAR,
                  'panel_content': panel_content}

    return panel.render(panel_vals)
