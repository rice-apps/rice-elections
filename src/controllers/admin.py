"""
Controller for admin related requests.
"""

import webapp2

from models.admin.organization_panel import OrganizationPanelHandler
from models.admin.organization_panel.election_panel import ElectionPanelHandler

app = webapp2.WSGIApplication([
    ('/admin/organization-panel', OrganizationPanelHandler),
    ('/admin/organization-panel/election-panel', ElectionPanelHandler),
], debug=True)