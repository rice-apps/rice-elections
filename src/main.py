"""
The Rice Elections App.
"""

__author__ = 'Waseem Ahmad (waseem@rice.edu)'

import jinja2
import os
import webapp2

from gaesessions import get_current_session

MAIN_DIR = os.path.dirname(__file__)
PAGES_DIR = os.path.join(MAIN_DIR, 'pages')

JINJA_ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(PAGES_DIR))

NAV_BAR = [
    {'text': 'Home', 'link': 'home'},
    {'text': 'Vote', 'link': 'vote'},
    {'text': 'Create Election', 'link': 'create'},
    {'text': 'Contact', 'link': 'contact'}]

class StaticHandler(webapp2.RequestHandler):
    """Handles GET requests for static pages."""
    def get(self):
        render_page(self, self.request.path, {})


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
    
    # If logged in, display NetID with logout option
    session = get_current_session()
    if session.has_key('net_id'):
        template_vals['net_id'] = session['net_id']
    
    handler.response.out.write(template.render(template_vals))

app = webapp2.WSGIApplication([
    ('/.*', StaticHandler)
], debug=True)
