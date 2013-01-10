"""
Database for the app.
"""

__author__ = 'Waseem Ahmad (waseem@rice.edu)'

import logging

from datetime import datetime
from google.appengine.ext import db

# Temporary look-up table until NetID input for candidates is implemented in the frontend
net_id_lookup = {'Waseem Ahmad': 'wa1',
                 'Sal Testa': 'srt6',
                 'Andrew Capshaw': 'apc3'}


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
    organization = db.ReferenceProperty(Organization,
                                        collection_name='elections')
    eligible_voters = db.ListProperty(db.Key)


class Voter(db.Model):
    """
    A voter that uses the application.
    """
    net_id = db.StringProperty()
    _election_keys = db.ListProperty(db.Key)     # List of elections user is eligible to vote in
    
    @property
    def elections(self):
        """
        Returns:
            election_list: a list of Elections the Voter is eligible to vote for.
        """
        election_list = []
        for election_key in self._election_keys:
            election_list.append(db.get(election_key))
        return election_list

    def add_election(self, election):
        """
        Makes the Voter eligible to vote in the specified election.
        
        Args:
            election: Election to add.
        """
        self._election_keys.append(election.key())
        self.put()


class Position(db.Model):
    """
    A position within an organization for which elections are held.
    """
    name = db.StringProperty()
    organization = db.ReferenceProperty(Organization,
                                        collection_name='positions')

class ElectionPosition(db.Model):
    """
    A position for a specific election within an organization.
    """
    election = db.ReferenceProperty(Election,
                                    collection_name='election_positions')
    position = db.ReferenceProperty(Position)
    slots = db.IntegerProperty()
    write_in = db.BooleanProperty()
    type = db.StringProperty(choices=('Single-Choice', 'Ranked-Choice'))
    candidates = db.ListProperty(db.Key)
    
class Candidate(db.Model):
    """
    A candidate for any election.
    """
    name = db.StringProperty()
    net_id = db.StringProperty()
    
    
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
        brown = Organization(name=name,
                             description='The best residential college.',
                             website='http://brown.rice.edu')
        brown.put()
        return brown
    
    return None


def put_election(name, start, end, organization):
    """
    Creates and stores an Election in the database.
    
    Args:
        name: election name.
        start: start time in time since epoch
        end: end time in time since epoch
        organization: the election Organization
        
    Returns:
        election: the Election object stored in the database
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
    election.organization = organization.key()
    election.put()
    logging.info('Election stored.')
    return election


def add_eligible_voters(election, net_id_list):
    """
    Adds the specified people as eligible voters for the election provided. Creates and stores a
    Voter entry for NetIDs who currently do not have a corresponding voter.
    
    Args:
        election: Election object to add eligible voters for.
        net_id_list: List of NetID strings
    """
    for net_id in net_id_list:
        voter = get_voter(net_id, create=True)
        voter.add_election(election)


def get_voter(net_id, create=False):
    """
    Returns the Voter entry for the NetID specified.
    
    Args:
        net_id {String}: NetID of the Voter.
        create {Boolean, optional}: Creates and stores a Voter entry if one doesn't exist.
    
    Returns:
        voter: The Voter entry corresponding to net_id, None if one doesn't exist and create is False.
    """
    query_result = db.GqlQuery('SELECT * FROM Voter WHERE net_id=:1 LIMIT 1', net_id).run()
    for voter in query_result:
        return voter
    
    if create:
        voter = Voter(net_id=net_id)
        voter.put()
        logging.info('Voter with NetID: %s created and stored.', net_id)
        return voter
    
    return None


def get_position(name, organization, create=False):
    """
    Returns the named Position from the specified organization.
    
    Args:
        name {String}: the name of the position
        organization {db.Model}: Organization of the position
        create {Boolean, optional}: Creates and stores a Position if one doesn't exist.
        
    Returns:
        position {db.Model}: The Position entry in the database, None if one doesn't exist and create is False.
    """
    position = db.GqlQuery('SELECT * FROM Position WHERE organization=:1 AND name=:2', organization, name).get()
    if not position and create:
        position = Position(name=name, organization=organization.key())
        position.put()
        logging.info('Position created with name: %s for organization: %s', name, organization.name)
    return position


def get_candidate(name, net_id, create=False):
    """
    Returns the candidate with the specified net_id.
    
    Args:
        name {String}: the name of the candidate
        net_id {String}: the NetID of the candidate
    
    Returns:
        Candidate {db.Model}: The Candidate entry in the database, None if one doesn't exist and create is False.
    """
    candidate = db.GqlQuery('SELECT * FROM Candidate WHERE net_id=:1', net_id).get()
    if not candidate and create:
        candidate = Candidate(name=name, net_id=net_id)
        candidate.put()
        logging.info('Candidate created with name: %s NetID: %s', name, net_id)
    return candidate


def put_election_position(election, position, slots, write_in, position_type):
    """
    Creates and stores an ElectionPosition in the database.
    
    Args:
        election {db.Model}: the Election for which this ElectionPosition is being created.
        position {db.Model}: the Position entry corresponding to the ElectionPosition.
        slots {Integer}: the number of slots for this position.
        write_in {Boolean}: whether a write-in is allowed.
        position_type {String}: the position type, see entity definition for choices.
    
    Returns:
        election_position {db.Model}: the ElectionPosition that was stored in the database.
    """
    election_position = ElectionPosition(election=election.key(),
                                         position=position.key(),
                                         slots=slots,
                                         write_in=write_in,
                                         type=position_type)
    election_position.put()
    logging.info('ElectionPosition created for %s in organization: %s', 
                        election_position.position.name, election_position.position.organization.name)
    return election_position


def put_candidate_for_election_position(candidate, election_position):
    """
    Adds a candidate as a runner for the specified election_position.
    
    Args:
        candidate {db.Model}: the Candidate
        election_position {db.Model}: the ElectionPosition the Candidate is running for
    """
    election_position.candidates.append(candidate.key())
    election_position.put()