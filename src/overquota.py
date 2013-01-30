"""
Message for quota exceeded.
"""

__author__ = 'Waseem Ahmad <waseem@rice.edu>'


import webapp2

from main import render_page

class OverQuotaHandler(webapp2.RequestHandler):

    def get(self):
        msg = ('Dear Voters,<br><br>'
               'It turns out we have ran out of our quota for the application. '
               'We did not anticipate so much traffic and are currently working '
               'hard trying '
               'to sort out billing with Google to bring the app back up. We '
               'will extend the voting time if need be and  make sure that '
               'everyone gets a chance to vote.<br><br>'
               'We apologize for the inconvenience.<br><br>'
               'Sincerely,<br><br>'
               'Owlection Team')
        render_page(self, '/message', {'status': 'Oh no!', 'msg': msg})
        return

app = webapp2.WSGIApplication([
        ('/.*', OverQuotaHandler),
], debug=True)