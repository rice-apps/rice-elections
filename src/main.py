"""
The Rice Elections App.
"""

__author__ = 'Waseem Ahmad <waseem@rice.edu>'


import datetime
import jinja2
import os
import webapp2

from gaesessions import get_current_session

MAIN_DIR = os.path.dirname(__file__)
PAGES_DIR = os.path.join(MAIN_DIR, 'pages')

JINJA_ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(PAGES_DIR))

NAV_BAR = [
    {'text': 'Home', 'link': '/home'},
    {'text': 'Vote', 'link': '/vote'},
    {'text': 'Admin', 'link': '/organization-panel'},
    {'text': 'Contact', 'link': '/contact'}]

class StaticHandler(webapp2.RequestHandler):
    """Handles GET requests for static pages."""
    def get(self):
        render_page(self, self.request.path, {})


def render_page(handler, page_name, page_data):
    page = get_page(page_name, page_data)

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

def render_html(handler, page_name, page_data):
    handler.response.out.write(get_page(page_name, page_data))

def get_page(page_name, page_data):
    # Add Jinja Filters
    JINJA_ENV.filters['datetime'] = format_datetime
    JINJA_ENV.globals['now'] = datetime.datetime.now()

    # Get the page name being requested assume home.html if none specified
    if page_name == '/':
        page_name += NAV_BAR[0]['link']
    
    # Get page info
    try:
        page = JINJA_ENV.get_template(page_name + '.html').render(page_data)
    except jinja2.TemplateNotFound:
        page = JINJA_ENV.get_template('not-found.html').render()

    return page

def format_datetime(value, format):
    if format == 'medium':
        return value.strftime('%a, %B %d, %Y, %I:%M %p') + ' UTC'
    if format == 'small':
        return value.strftime('%m/%d/%y %I:%M %p') + ' UTC'

app = webapp2.WSGIApplication([
    ('/.*', StaticHandler)
], debug=True)
