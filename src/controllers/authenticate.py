"""
Controller for authentication related requests.
"""

import webapp2

from authentication.auth import LoginResponseHandler
from authentication.auth import LogoutHandler
from authentication.auth import LogoutResponseHandler
from authentication.cleanupsessions import CleanupSessionsHandler

app = webapp2.WSGIApplication([
    ('/authenticate/login-response', LoginResponseHandler),
    ('/authenticate/logout', LogoutHandler),
    ('/authenticate/logout-response', LogoutResponseHandler),
    ('/authenticate/cleanup-sessions', CleanupSessionsHandler)
], debug=True)