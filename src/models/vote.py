"""
Back-end for the vote page.
"""

__authors__ = ['Waseem Ahmad <waseem@rice.edu>',
               'Andrew Capshaw <capshaw@rice.edu>']

import datetime
import logging
import models
import webapp2
import webapputils

from authentication import auth


class VoteHandler(webapp2.RequestHandler):
    """
    Handles GET requests for the Vote page.
    """

    def get(self):
        page_data = {'open_elections': [], 'election_results': []}

        # Authenticate user
        voter = auth.get_voter(self)

        # Elections the user is eligible to vote for
        elections = voter.elections
        election_keys = [election.key() for election in elections]

        # Add universal elections
        universal_elections = models.Election.gql("WHERE universal=TRUE AND hidden=FALSE")
        for election in universal_elections:
            if datetime.datetime.now() < election.end and election.key() not in election_keys:
                elections.append(election)

        logging.info(elections)

        for election in elections:
            logging.info('Found election')
            data = {}
            data['id'] = str(election.key())
            data['name'] = election.name
            data['organization'] = election.organization.name
            now = datetime.datetime.now()
            if now > election.end:      # Election passed
                result_delay = election.result_delay
                data['end_date'] = election.end.strftime('%a, %B %d, %Y, %I:%M %p') + ' UTC'
                data['result_delay'] = result_delay

                # Compute how much time the user will have to wait to view the election
                time_since_election_end = (now - election.end).seconds + (now - election.end).days * 86400
                if time_since_election_end > result_delay:
                    data['time_remaining'] = -1
                else:
                    data['time_remaining'] = (result_delay - time_since_election_end) *1000
                page_data['election_results'].append(data)
            else:
                data['user_action'] = 'not_started' # Initial assumption

                # Check election times
                if election.start > now:
                    start_str = election.start.strftime('%a, %B %d, %Y, %I:%M %p') + ' UTC'
                    data['status'] = {'text': 'Voting begins on', 'date': start_str}
                    data['user_action'] = 'not_started'
                else:
                    end_str = election.end.strftime('%a, %B %d, %Y, %I:%M %p') + ' UTC'
                    data['status'] = {'text': 'Voting ends on', 'date': end_str}
                    data['user_action'] = 'vote'

                # Check to see if the user has already voted
                if models.voter_status(voter, election) == 'voted':
                    data['user_action'] = 'voted'

                page_data['open_elections'].append(data)
            logging.info(data)

        webapputils.render_page(self, '/vote', page_data)


app = webapp2.WSGIApplication([
        ('/vote', VoteHandler)
], debug=True)