"""
Back-end for the Election Panel.
"""

__author__ = 'Waseem Ahmad <waseem@rice.edu>'

import json
import logging
import webapp2

from authentication import auth
from datetime import datetime, timedelta
from google.appengine.api import taskqueue
from google.appengine.ext import db
from main import render_html, render_page, render_page_content, get_page, JINJA_ENV
from models import models

PAGE_NAME = '/admin/organization-panel/election-panel'
MSG_NOT_AUTHORIZED = ('We\'re sorry, you\'re not an organization administrator.'
    ' Please contact the website administration if you are interested in '
    'conducting elections for your organization.')
PANEL_BAR = [
    {'text': 'Election Information', 'link': PAGE_NAME+'/information'},
    {'text': 'Positions', 'link': PAGE_NAME+'/positions'},
    {'text': 'Voters', 'link': PAGE_NAME+'/voters'}]


class ElectionPanelHandler(webapp2.RequestHandler):
    
    def get(self):
        # Authenticate user
        voter = auth.get_voter(self)
        status = models.get_admin_status(voter)
        if not status:
            render_page(self, '/templates/message',
                        {'status': 'Not Authorized', 'msg': MSG_NOT_AUTHORIZED})
            return

        election = None
        election_id = self.request.get('id')
        if election_id:
            election = models.Election.get(election_id)
            if not election:
                render_page(self, '/templates/message',
                    {'status': 'Error', 'msg': 'Election not found.'})
                return
            auth.set_election(election)
        else:
            auth.clear_election()

        # Construct page information
        if (self.request.path.endswith('/election-panel') or 
            self.request.path.endswith('/election-panel/')):
            panel = get_panel(PAGE_NAME + '/information', {}, election_id)
        else:
            panel = get_panel(self.request.path, {}, election_id)
        render_page_content(self, PAGE_NAME, panel)


def get_panel(page_name, page_data, election_id=None):
    """
    Renders the election panel with the specified sub page and data.

    Args:
        page_name {String}: the name of the panel page
        page_data {Dictionary}: the data for the specified page
        election_id {String, Optional}: the ID of the election
    """
    panel_content = get_page(page_name, page_data)
    # Mark all links in the panel bar as inactive except the page open
    for item in PANEL_BAR:
        item['active'] = page_name.startswith(item['link'])

    panel = JINJA_ENV.get_template(
        'admin/organization-panel/election-panel.html')
    panel_vals = {'id': election_id,
                  'panel_bar': PANEL_BAR,
                  'panel_content': panel_content}

    return panel.render(panel_vals)
