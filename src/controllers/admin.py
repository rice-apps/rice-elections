"""
Controller for admin related requests.
"""

import webapp2

from models.admin.organization_panel import OrganizationPanelHandler
from models.admin.organization_panel.election_panel import ElectionPanelHandler
from models.admin.organization_panel.election_panel.information import ElectionInformationHandler
from models.admin.organization_panel.election_panel.voters import ElectionVotersHandler

app = webapp2.WSGIApplication([
    ('/admin/organization-panel', OrganizationPanelHandler),
    ('/admin/organization-panel/election-panel', ElectionPanelHandler),
    ('/admin/organization-panel/election-panel/information', ElectionInformationHandler),
    ('/admin/organization-panel/election-panel/voters', ElectionVotersHandler),
    ('/admin/organization-panel/election-panel/.*', ElectionPanelHandler)
], debug=True)