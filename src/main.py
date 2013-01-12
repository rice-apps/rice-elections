"""
The Rice Elections App.
"""

__author__ = 'Waseem Ahmad (waseem@rice.edu)'

import jinja2
import logging
import os
import pycas
import webapp2

MAIN_DIR = os.path.dirname(__file__)
PAGES_DIR = os.path.join(MAIN_DIR, 'pages')

JINJA_ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(PAGES_DIR))

CAS_SERVER  = "https://netid.rice.edu"

NAV_BAR = [
    {'text': 'Home', 'link': 'home'},
    {'text': 'Vote', 'link': 'vote'},
    {'text': 'Create Election', 'link': 'create'},
    {'text': 'Contact', 'link': 'contact'}]

class StaticHandler(webapp2.RequestHandler):
    """Handles GET requests for static pages."""
    def get(self):
        render_page(self, self.request.path, {})


def require_login(request_handler):
    """
    Requires the user to be logged in through NetID authentication.

    Args:
        request_handler: webapp2 request handler of the user request

    Returns:
        net_id: the NetID of the user
    """
    service_url = request_handler.request.url
    if '?ticket=' in service_url:
        ticket_i = service_url.index('?ticket')
        remaining_i = service_url[ticket_i:].index('?')
        if remaining_i > 0:
            service_url = service_url[0:ticket_i] + service_url[remaining_i:]
        else:
            service_url = service_url[0:ticket_i]
    status, net_id, cookie = pycas.login(CAS_SERVER, service_url, request_handler)
    logging.info('CAS Authentication Status: %s NetID: %s Cookie:%s', status, net_id, cookie)
    return net_id


def render_page(handler, page_name, page_data):
    # Get the page name being requested assume home.html if none specified
    if page_name == '/':
        page_name += NAV_BAR[0]['link']

    # Get page info
    try:
        page = JINJA_ENV.get_template(page_name + '.html').render(page_data)
    except Exception:
        page = JINJA_ENV.get_template('not-found.html').render()

    # Mark all links in the nav bar as inactive except the page open
    for item in NAV_BAR:
        if '/'+item['link'] == page_name:
            item['active'] = True
        else:
            item['active'] = False

    template = JINJA_ENV.get_template('template.html')
    template_vals = {'nav_bar': NAV_BAR,
                     'page_content': page}
    handler.response.out.write(template.render(template_vals))

app = webapp2.WSGIApplication([
    ('/.*', StaticHandler)
], debug=True)
