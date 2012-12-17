"""
The Rice Elections App.
"""

__author__ = 'Waseem Ahmad (waseem@rice.edu)'

import jinja2
import logging
import os
import webapp2

MAIN_DIR = os.path.dirname(__file__)
PAGES_DIR = os.path.join(MAIN_DIR, 'pages')

JINJA_ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(PAGES_DIR))

NAV_BAR = [
    {'text': 'Home', 'link': 'index.html'},
    {'text': 'Contact', 'link': 'contact.html'}]

class MainHandler(webapp2.RequestHandler):
    def get(self):
        logging.info('Requested URL: %s', self.request.path)

        # Get the page name being requested
        # assume index.html if none specified
        page_name = self.request.path
        if page_name == '/':
            page_name = NAV_BAR[0]['link']

        # Get page info
        try:
            page = JINJA_ENV.get_template(page_name).render()
        except Exception as e:
            page = JINJA_ENV.get_template('not_found.html').render()

        # Mark all links in the nav bar as inactive except the page open
        for item in NAV_BAR:
            if '/'+item['link'] == page_name:
                item['active'] = True
            else:
                item['active'] = False

        template = JINJA_ENV.get_template('template.html')
        template_vals = {'nav_bar': NAV_BAR,
                         'page_content': page}
        self.response.out.write(template.render(template_vals))

app = webapp2.WSGIApplication([
    ('/.*', MainHandler)
], debug=True)
