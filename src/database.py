"""
Database for the app.
"""

__author__ = 'Waseem Ahmad (waseem@rice.edu)'

import logging

from datetime import datetime
from google.appengine.ext import db


class Organization(db.Model):
    """
    An organization that uses this application to host elections.
    Organizations are tied to individual Elections and OrganizationPositions.
    """
    name = db.StringProperty()
    description = db.TextProperty()
    website = db.StringProperty()

def get_organization(name):
    """
    Returns the organization the election data is referring to.
    
    Args:
        name: The name of the organization.
    
    Returns:
        Organization from database. None if it doesn't exist.
    """
    temp_hard_code = True
    
    if not name:
        if temp_hard_code:
            name = 'Brown College'
        else:
            return None
    
    query_result = db.GqlQuery('SELECT * FROM Organization WHERE name=:1 LIMIT 1', name).run()
    for organization in query_result:
        return organization
    
    # Create Brown College organization
    if temp_hard_code:
        brown = Organization()
        brown.name = name
        brown.description = 'The best residential college.'
        brown.website = 'http://brown.rice.edu'
        brown.put()
        return brown
    
    return None

class Election(db.Model):
    """
    An election that users may vote for.
    """
    name = db.StringProperty()
    start = db.DateTimeProperty()       # Time when voting begins
    end = db.DateTimeProperty()         # Time when voting ends
    organization = Organization()       # The organization holding the election

def put_election(name, start, end, organization):
    """
    Creates and stores an election in the database.
    
    Args:
        name: election name.
        start: start time in time since epoch
        end: end time in time since epoch
        organization: the election Organization
    """
    for arg in [name, start, end, organization]:
        if not arg:
            raise Exception('One or more args missing')
    logging.info('Storing new election: %s, start: %s, end: %s, organization: %s',
                 name, start, end, organization.name)
    election = Election()
    election.name = name
    election.start = datetime.fromtimestamp(start)
    election.end = datetime.fromtimestamp(end)
    election.organization = organization
    election.put()
    logging.info('Election stored.')

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
    
