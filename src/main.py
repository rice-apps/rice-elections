"""
The Rice Elections App.
"""

__author__ = 'Waseem Ahmad (waseem@rice.edu)'

import jinja2
import json
import logging
import os
import webapp2

MAIN_DIR = os.path.dirname(__file__)
PAGES_DIR = os.path.join(MAIN_DIR, 'pages')

JINJA_ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(PAGES_DIR))

NAV_BAR = [
    {'text': 'Home', 'link': 'home'},
    {'text': 'Vote', 'link': 'vote'},
    {'text': 'Create Election', 'link': 'create'},
    {'text': 'Contact', 'link': 'contact'}]

class MainHandler(webapp2.RequestHandler):
    def get(self):
        logging.info('Requested URL: %s', self.request.path)

        # Get the page name being requested
        # assume home.html if none specified
        page_name = self.request.path
        if page_name == '/':
            page_name += NAV_BAR[0]['link']

        # Get the data for the page from the database
        page_data = {}
        if page_name == '/vote':
            # TODO: get this data from the database
            page_data = {'open_elections': [{'name' : 'Brown Spring Elections',
                                             'start': 'Mar 11 @ 9:00 am',
                                             'end': 'Mar 12 @ 9:00 am',
                                             'organization': 'Brown College'},
                                             {'name' : 'Ballot Initiative 82',
                                             'start': 'Feb 9 @ 10:00 am',
                                             'end': 'Feb 10 @ 10:00 am',
                                             'organization': 'Rice Student Association'}]}

        # Get page info
        try:
            page = JINJA_ENV.get_template(page_name + '.html').render()
        except Exception:
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
