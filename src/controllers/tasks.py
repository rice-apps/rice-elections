"""
Controller for tasks.
Routed through here for security reasons, ensures the tasks were internally
generated and not by a user.
"""

import webapp2

from models.admin_.organization_.election_.information import ElectionTaskHandler
from models.admin_.organization_.election_.voters import ElectionVotersTaskHandler

app = webapp2.WSGIApplication([
    ('/tasks/admin/organization/election/information', ElectionTaskHandler),
    ('/tasks/admin/organization/election/voters', ElectionVotersTaskHandler)
], debug=True)