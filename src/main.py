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


class VotesCountHandler(webapp2.RequestHandler):
    def get(self):
        votes_count = models.get_vote_count()
        self.response.write(json.dumps({'votes_count': votes_count}))


app = webapp2.WSGIApplication([
    ('/stats/votes-count', VotesCountHandler),
    ('/.*', StaticHandler)
], debug=True)