"""
Database for the app.
"""

__author__ = 'Waseem Ahmad (waseem@rice.edu)'

from google.appengine.ext import db


class Organization(db.Model):
    """
    An organization that uses this application to host elections.
    Organizations are tied to individual Elections and OrganizationPositions.
    """
    name = db.StringProperty()
    description = db.TextProperty()
    website = db.StringProperty()


class Election(db.Model):
    """
    An election that users may vote for.
    """
    name = db.StringProperty()
    start = db.DateTimeProperty()       # Time when voting begins
    end = db.DateTimeProperty()         # Time when voting ends
    organization = Organization()       # The organization holding the election


class Voter(db.Model):
    """
    A voter that uses the application.
    """
    net_id = db.StringProperty()
    

class EligibleVoter(db.Model):
    """
    An entity that represents an election that an individual voter is eligible to vote for.
    """
    voter = Voter()
    election = Election()
    
