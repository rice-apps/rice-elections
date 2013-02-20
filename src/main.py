"""
The Rice Elections App.
"""

__author__ = 'Waseem Ahmad <waseem@rice.edu>'


import logging
import json
import webapp2

from google.appengine.api import memcache
from models import models, webapputils

NAV_BAR = [
    {'text': 'Home', 'link': '/home'},
    {'text': 'Vote', 'link': '/vote'},
    {'text': 'Admin', 'link': '/admin/organization'},
    {'text': 'Contact', 'link': '/contact'}]

class StaticHandler(webapp2.RequestHandler):
    """Handles GET requests for static pages."""
    def get(self):
        webapputils.render_page(self, self.request.path, {})


class BallotsCastCountHandler(webapp2.RequestHandler):
    def get(self):
        ballots_cast = memcache.get('ballots-cast-count')
        if not ballots_cast:
            query = models.ElectionVoter.gql('WHERE vote_time!=NULL')
            ballots_cast = query.count()
            memcache.set('ballots-cast-count', ballots_cast, 9)
        self.response.write(json.dumps({'ballots_cast': ballots_cast}))


app = webapp2.WSGIApplication([
    ('/stats/ballot-count', BallotsCastCountHandler),
    ('/.*', StaticHandler)
], debug=True)