"""
Controller for admin related requests.
"""

import webapp2

from models.admin_.organization_panel import OrganizationPanelHandler
from models.admin_.organization_panel_.election_panel import ElectionPanelHandler
from models.admin_.organization_panel_.election_panel_.information import ElectionInformationHandler
from models.admin_.organization_panel_.election_panel_.voters import ElectionVotersHandler

app = webapp2.WSGIApplication([
    ('/admin/organization-panel', OrganizationPanelHandler),
    ('/admin/organization-panel/election-panel', ElectionPanelHandler),
    ('/admin/organization-panel/election-panel/information', ElectionInformationHandler),
    ('/admin/organization-panel/election-panel/voters', ElectionVotersHandler),
    ('/admin/organization-panel/election-panel/.*', ElectionPanelHandler)
], debug=True)