"""
Controller for admin related requests.
"""

import webapp2

from models.admin_.organization import OrganizationPanelHandler
from models.admin_.organization_.election import ElectionPanelHandler
from models.admin_.organization_.election_.information import ElectionInformationHandler
from models.admin_.organization_.election_.positions import ElectionPositionsHandler
from models.admin_.organization_.election_.voters import ElectionVotersHandler

app = webapp2.WSGIApplication([
    ('/admin/organization', OrganizationPanelHandler),
    ('/admin/organization/election', ElectionPanelHandler),
    ('/admin/organization/election/information', ElectionInformationHandler),
    ('/admin/organization/election/positions', ElectionPositionsHandler),
    ('/admin/organization/election/voters', ElectionVotersHandler),
    ('/admin/organization/election/.*', ElectionPanelHandler)
], debug=True)