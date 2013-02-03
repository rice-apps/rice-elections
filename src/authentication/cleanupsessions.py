import webapp2
from gaesessions import delete_expired_sessions

class CleanupSessionsHandler(webapp2.RequestHandler):
    def get(self):
        while not delete_expired_sessions():
            pass

