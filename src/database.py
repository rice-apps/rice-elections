"""
Database for the app.
"""

__author__ = 'Waseem Ahmad (waseem@rice.edu)'

import irv
import logging

from datetime import datetime
from google.appengine.ext import db
from google.appengine.ext.db import polymodel


class Organization(db.Model):
    """
    An organization that uses this application to host elections.
    Organizations are tied to individual Elections and OrganizationPositions.
    """
    name = db.StringProperty(required=True)
    description = db.TextProperty()
    website = db.StringProperty()


class Election(db.Model):
    """
    An election that users may vote for.
    """
    name = db.StringProperty(required=True)
    start = db.DateTimeProperty(required=True)       # Time when voting begins
    end = db.DateTimeProperty(required=True)         # Time when voting ends
    organization = db.ReferenceProperty(Organization,
                                        collection_name='elections')
    result_computed = db.BooleanProperty(required=True,
                                         default=False)
    result_delay = db.IntegerProperty(required=True,
                                      default=0) # Results delay to public in seconds

    def to_json(self):
        """
        Creates a JSON object of the election to pass to the client side.
        """
        return {
            'id': str(self.key()),
            'name': self.name,
            'organization': self.organization.name
        }


class Voter(db.Model):
    """
    A voter that uses the application.
    """
    net_id = db.StringProperty(required=True)
    
    @property
    def elections(self):
        """
        Returns:
            election_list: a list of Elections the Voter is eligible to vote for.
        """
        election_list = []
        for election_voter in ElectionVoter.gql('WHERE voter=:1', self.key()):
            election_list.append(election_voter.election)
        return election_list


class Admin(db.Model):
    """
    An election administrator for the application.
    """
    email = db.StringProperty(required=True)
    voter = db.ReferenceProperty(Voter,
                                 required=True)


class OrganizationAdmin(db.Model):
    """
    An Admin that manages elections for an Organization.
    """
    admin = db.ReferenceProperty(Admin,
                                 required=True,
                                 collection_name='organization_admins')
    organization = db.ReferenceProperty(Organization,
                                        required=True,
                                        collection_name='organization_admins')

class ElectionVoter(db.Model):
    """
    A Voter that is eligible to vote for a specific election.
    """
    voter = db.ReferenceProperty(Voter,
                                 required=True,
                                 collection_name='election_voters')
    election = db.ReferenceProperty(Election,
                                    required=True,
                                    collection_name='election_voters')
    vote_time = db.DateTimeProperty()       # Time when user casted a vote


class Position(db.Model):
    """
    A position within an organization for which elections are held.
    """
    name = db.StringProperty(required=True)
    organization = db.ReferenceProperty(Organization,
                                        required=True,
                                        collection_name='positions')


class ElectionPosition(polymodel.PolyModel):
    """
    A position for a specific election within an organization.
    """
    election = db.ReferenceProperty(Election,
                                    collection_name='election_positions',
                                    required=True)
    position = db.ReferenceProperty(Position,
                                    required=True)
    vote_required = db.BooleanProperty(required=True)
    write_in_slots = db.IntegerProperty(required=True)
    winners = db.ListProperty(db.Key)

    def to_json(self):
        """
        Creates a JSON object of the election position to pass to the client
        side.
        """
        json = {
            'id': str(self.key()),
            'name': self.position.name,
            'write_in_slots': self.write_in_slots,
            'winners': [winner.to_json() for winner in self.winners],
            'candidates': []
        }
        for epc in self.election_position_candidates:
            if epc.written_in:
                continue
            json['candidates'].append({'name': epc.name,
                                       'id': str(epc.key())})
        return json

    def compute_winners(self):
        """
        Computes the winners of this election position.
        """
        assert datetime.now() > self.election.end
        assert not self.election.result_computed


class RankedVotingPosition(ElectionPosition):
    """
    A position that requires ranked voting.
    """
    position_type = 'Ranked-Choice'

    def to_json(self):
        """
        Creates a JSON object of the election position to pass to the client
        side.
        """
        json = super(RankedVotingPosition, self).to_json()
        json['type'] = self.position_type
        return json

    def compute_winners(self):
        ballots = []
        for ballot in self.ballots:
            ballots.append(ballot.preferences)
        
        winners = irv.run_irv(ballots)
        for winner in winners:
            self.winners.append(winner)

class CumulativeVotingPosition(ElectionPosition):
    """
    A position that requires cumulative voting.
    """
    position_type = 'Cumulative'
    points = db.IntegerProperty(required=True)
    slots = db.IntegerProperty(required=True)

    def to_json(self):
        """
        Creates a JSON object of the election position to pass to the client
        side.
        """
        json = super(CumulativeVotingPosition, self).to_json()
        json['type'] = self.position_type
        json['points'] = self.points
        json['slots'] = self.slots
        return json

    def compute_winners(self):
        raise NotImplementedError('Later')
    
# class ElectionPositionOld(db.Model):
#     """
#     A position for a specific election within an organization.
#     """
#    election = db.ReferenceProperty(Election,
#                                    collection_name='election_positions')
#    position = db.ReferenceProperty(Position)
#    slots = db.IntegerProperty(required=True,
#                               default=1)
#    write_in = db.BooleanProperty(required=True)
#    vote_required = db.BooleanProperty(required=True)
#    type = db.StringProperty(choices=('Single-Choice', 'Ranked-Choice'))


class ElectionPositionCandidate(db.Model):
    """
    A candidate running for an election position.
    """
    election_position = db.ReferenceProperty(ElectionPosition,
                                             required=True,
                                             collection_name='election_position_candidates')
    net_id = db.StringProperty()
    name = db.StringProperty(required=True)
    written_in = db.BooleanProperty(required=True, default=False)


class RankedBallot(db.Model):
    """
    A single ranked ballot for an election position.
    """
    position = db.ReferenceProperty(RankedVotingPosition,
                                    required=True,
                                    collection_name='ballots')
    preferences = db.ListProperty(db.Key,
                                  required=True)


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


def put_admin(voter, email, organization):
    """
    Makes a Voter an Admin of the specified organization.
    
    Args:
        voter {Voter}: the user of the website
        email {String}: the email address of the admin
        organization {Organization}: the organization to make Admin of.
    
    Returns:
        {OrganizationAdmin}: the OrganizationAdmin entity.
    """
    admin = Admin(voter=voter, email=email).put()
    return OrganizationAdmin(admin=admin, organization=organization).put()


def get_admin_status(voter, organization=None):
    """
    Returns whether the voter is an Admin. If organization specified, will check to see if voter is an Admin for the
    organization.
    
    Args:
        voter {Voter}: the user of the website
        organization {Organization, optional}: the organization to check against
        
    Returns:
        True if Admin, False otherwise.
    """
    admin = Admin.gql('WHERE voter=:1', voter).get()
    if not admin:
        return False
    if organization:
        organization_admin = OrganizationAdmin.gql('WHERE admin=:1 AND organization=:2', admin, organization).get()
        if not organization_admin:
            return False
    return True


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
    election = Election(name=name,
                        start=datetime.fromtimestamp(start),
                        end=datetime.fromtimestamp(end),
                        organization=organization.key())
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
        ElectionVoter(voter=voter,
                      election=election).put()


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


def put_election_position(election, position, slots, write_in, position_type, vote_required):
    """
    Creates and stores an ElectionPosition in the database.
    
    Args:
        election {db.Model}: the Election for which this ElectionPosition is being created.
        position {db.Model}: the Position entry corresponding to the ElectionPosition.
        slots {Integer}: the number of slots for this position.
        write_in {Boolean}: whether a write-in is allowed.
        position_type {String}: the position type, see entity definition for choices.
        vote_required {Boolean}: whether a voter is required to vote for this position.
    
    Returns:
        election_position {db.Model}: the ElectionPosition that was stored in the database.
    """
    election_position = ElectionPosition(election=election.key(),
                                         position=position.key(),
                                         slots=slots,
                                         write_in=write_in,
                                         type=position_type,
                                         vote_required=vote_required)
    election_position.put()
    logging.info('ElectionPosition created for %s in organization: %s', 
                        election_position.position.name, election_position.position.organization.name)
    return election_position


def get_candidates_for_election_position(election_position):
    """
    Gets the candidates running for an election position.
    
    Args:
        election_position {ElectionPosition}: the ElectionPosition
    
    Returns:
        candidates {Iterator<ElectionPositionCandidate>}: the candidates running
    """
    return ElectionPositionCandidate.gql('WHERE election_position=:1', election_position).run()
    

def put_candidate_for_election_position(election_position, name, net_id=None, written_in=False):
    """
    Adds a candidate as a runner for the specified election_position.
    
    Args:
        election_position {ElectionPosition}: the ElectionPosition the Candidate is running for
        name {String}: the name of the candidate
        net_id {String, optional}: the NetID of the candidate
        written_in {Boolean, optional}: whether the candidate was written in.
    """
    ElectionPositionCandidate(election_position=election_position.key(), 
                              name=name,
                              net_id=net_id,
                              written_in=written_in).put()


def voter_status(voter, election):
    """
    Tells the voter status for a specific election.
    
    Args:
        voter {Voter}: the Voter
        election {Election}: the Election
    
    Returns:
        status {String}: 'not_eligible', 'eligible', 'invalid_time', or 'voted'
    """
    election_voter = ElectionVoter.gql('WHERE voter=:1 AND election=:2', voter, election).get()
    if not election_voter:
        return 'not_eligible'
    elif election_voter.vote_time:
        return 'voted'
    elif datetime.now() < election.start or datetime.now() > election.end:
        return 'invalid_time'
    else:
        return 'eligible'
    

def mark_voted(voter, election):
    """
    Marks the voter as having voted for a specific election.
    
    Args:
        voter {Voter}: the Voter
        election {Election}: the Election
    
    Returns:
        status {Boolean}: True if marked as voted successfully, False otherwise.
    """
    election_voter = ElectionVoter.gql('WHERE voter=:1 AND election=:2', voter, election).get()
    if not election_voter:
        return False
    election_voter.vote_time = datetime.now()
    election_voter.put()
    return True