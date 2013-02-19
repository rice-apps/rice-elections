"""
Back end for election panel positions.
"""

__author__ = 'Waseem Ahmad <waseem@rice.edu>'

import json
import logging
import webapp2

from authentication import auth
from models import models, webapputils
from models.admin_.organization_.election import get_panel

PAGE_NAME = '/admin/organization/election/positions'


class ElectionPositionsHandler(webapp2.RequestHandler):

    def get(self):
        # Authenticate user
        voter = auth.get_voter(self)
        status = models.get_admin_status(voter)
        if not status:
            webapputils.render_page(self, '/templates/message',
                {'status': 'Error', 'msg': 'Not Authorized'})
            return

        # Get election
        election = auth.get_election()
        if not election:
            panel = get_panel(
                PAGE_NAME,
                {'status': 'Error','msg': 'No election found.'},
                None)
            webapputils.render_page_content(self, PAGE_NAME, panel)
            return

        data = {'id': str(election.key())}
        panel = get_panel(PAGE_NAME, data, data.get('id'))
        webapputils.render_page_content(self, PAGE_NAME, panel)

    def post(self):
        methods = {
            'get_positions': self.get_positions,
            'add_position': self.add_position,
            'get_position': self.get_position
        }

        # Get election
        election = auth.get_election()
        if not election:
            return

        # Get the method
        data = json.loads(self.request.get('data'))
        method = data['method']
        logging.info('Method: %s\n Data: %s', method, data)
        if method in methods:
            methods[method](election, data)

    def get_positions(self, election, data):
        out = {'positions': [p.to_json() for p in election.election_positions]}
        self.response.write(json.dumps(out))

    def add_position(self, election, data):
        position = data['position']
        position_entry = models.get_position(position['name'],
                                             election.organization,
                                             create=True)

        # Store position
        if position['type'] == 'Ranked-Choice':
            ep = models.RankedVotingPosition(
                election=election,
                position=position_entry,
                vote_required=position['vote_required'],
                write_in_slots=position['write_in_slots'])
            ep.put()
        elif position['type'] == 'Cumulative-Voting':
            ep = models.CumulativeVotingPosition(
                election=election,
                position=position_entry,
                vote_required=position['vote_required'],
                write_in_slots=position['write_in_slots'],
                points=position['points'],
                slots=position['slots'])
            ep.put()

        # Store candidates
        for candidate in position['candidates']:
            models.ElectionPositionCandidate(
                election_position=ep,
                name=candidate['name']).put()

        out = {'status': 'OK',
               'msg': 'Created',
               'position': ep.to_json()}
        self.response.write(json.dumps(out))

    def get_position(self, election, data):
        position_entry = models.ElectionPosition.get(data['id'])
        if position_entry:
            self.response.write(json.dumps(
                {'position': position_entry.to_json()}))
            logging.info(position_entry.to_json())
        else:
            webapputils.respond(self, 'ERROR', 'Not found')

