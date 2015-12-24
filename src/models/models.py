"""
Database for the app.
"""

__author__ = 'Waseem Ahmad <waseem@rice.edu>'

import logging

from datetime import timedelta
from algorithms_ import cv, irv
from datetime import datetime
from google.appengine.ext import db
from google.appengine.api import memcache
from google.appengine.ext.db import polymodel


class Organization(db.Model):
    """
    An organization that uses this application to host elections.
    Organizations are tied to individual Elections and OrganizationPositions.
    """
    name = db.StringProperty(required=True)
    description = db.TextProperty()
    website = db.StringProperty()
    image = db.StringProperty()
    carousel_show_name = db.BooleanProperty(default=True)


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
    universal = db.BooleanProperty(required=True,
                                   default=False)
    hidden = db.BooleanProperty(required=True,
                                default=False)
    task_count = db.IntegerProperty(required=True,  # Counter used to identify tasks
                                    default=0)
    voter_count = db.IntegerProperty(required=True,
                                    default=0)
    voted_count = db.IntegerProperty(required=True,
                                     default=0)
    description = db.TextProperty(required=False, default="")
    def to_json(self, parseable_date=False):
        # calculate the publication date by adding result delay to end
        pub = self.end + timedelta(seconds=self.result_delay)
        # parseable_date means it can be parsed in JS with Date.parse()
        times = {
            'start': self.start.strftime('%a, %B %d, %Y, %I:%M %p') + ' UTC',
            'end': self.end.strftime('%a, %B %d, %Y, %I:%M %p') + ' UTC',
            'pub': pub.strftime('%a, %B %d, %Y, %I:%M %p') + ' UTC'
        } if parseable_date else {
            'start': str(self.start),
            'end': str(self.end),
            'pub': str(pub)
        }

        now = datetime.now()
        status = 'Not started'
        if now > self.start:
            status = 'Voting in progress'
        if now > self.end:
            status = 'Voting has ended'
        if self.result_computed:
            status = 'Result computed'

        return {
            'id': str(self.key()),
            'name': self.name,
            'organization': self.organization.name,
            'times': times,
            'result_computed': self.result_computed,
            'result_delay': self.result_delay,
            'universal': self.universal,
            'hidden': self.hidden,
            'voter_count': self.voter_count,
            'voted_count': self.voted_count,
            'description': self.description,
            'status': status,
        }

    @property
    def election_positions(self):
        return [ep for ep in ElectionPosition.gql(
            "WHERE election=:1 ORDER BY datetime_created", self)]


class Voter(db.Model):
    """
    A voter that uses the application.
    """
    net_id = db.StringProperty(required=True,
                               indexed=True)
    
    @property
    def elections(self):
        """
        Returns:
            election_list: a list of Elections the Voter is eligible to vote for.
        """
        election_list = []
        for election_voter in ElectionVoter.gql('WHERE voter=:1', self.key()):
            try:        # YOLO
                election_list.append(election_voter.election)
            except db.ReferencePropertyResolveError:
                election_voter.delete()     # Election no longer exists
        return election_list


class Admin(db.Model):
    """
    An election administrator for the application.
    """
    name = db.StringProperty()
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
                                 required=True)
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
                                    required=True)
    position = db.ReferenceProperty(Position,
                                    required=True)
    vote_required = db.BooleanProperty(required=True)
    write_in_slots = db.IntegerProperty(required=True)
    winners = db.ListProperty(db.Key)
    description = db.TextProperty(required=False, default="")
    datetime_created = db.DateTimeProperty(required=True, auto_now_add=True)
    result_computed = db.BooleanProperty(default=False)
    
    def to_json(self):
        json = {
            'id': str(self.key()),
            'name': self.position.name,
            'write_in_slots': self.write_in_slots,
            'vote_required': self.vote_required,
            'candidates': [],
            'description': self.description
        }
        for epc in self.election_position_candidates:
            logging.info(epc.name)
            if epc.written_in and epc.key() not in self.winners:
                continue
            candidate = {'name': epc.name,
                         'id': str(epc.key())}
            if epc.key() in self.winners:
                candidate['winner'] = True
            else:
                candidate['winner'] = False
            json['candidates'].append(candidate)
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
        json = super(RankedVotingPosition, self).to_json()
        json['type'] = self.position_type
        return json

    def compute_winners(self):
        super(RankedVotingPosition, self).compute_winners()
        ballots = []
        for ballot in self.ballots:
            ballots.append(ballot.preferences)
        
        winners = irv.run_irv(ballots)
        self.winners = []
        for winner in winners:
            self.winners.append(winner)
        self.result_computed = True
        self.put()

class CumulativeVotingPosition(ElectionPosition):
    """
    A position that requires cumulative voting.
    """
    position_type = 'Cumulative-Voting'
    points = db.IntegerProperty(required=True)
    slots = db.IntegerProperty(required=True)

    def to_json(self):
        json = super(CumulativeVotingPosition, self).to_json()
        json['type'] = self.position_type
        json['points'] = self.points
        json['slots'] = self.slots
        return json

    def compute_winners(self):
        super(CumulativeVotingPosition, self).compute_winners()
        ballots = []
        for ballot in self.ballots:
            ballot_dict = {}
            for choice in ballot.choices:
                candidate_key = choice.candidate.key()
                ballot_dict[candidate_key] = choice.points
            ballots.append(ballot_dict)
        winners = cv.run_cv(ballots, self.slots)
        self.winners = []
        for winner in winners:
            self.winners.append(winner)
        self.result_computed = True
        self.put()
    
class BooleanVotingPosition(ElectionPosition):
    """
    A position that requires each vote to be either yes or no.
    """
    position_type = 'Boolean-Voting'
    slots = db.IntegerProperty(required=True)

    def to_json(self):
        json = super(BooleanVotingPosition, self).to_json()
        json['type'] = self.position_type
        json['slots'] = self.slots
        return json

    def compute_winners(self):
        super(BooleanVotingPosition, self).compute_winners()
        ballots = []
        for ballot in self.ballots:
            ballot_dict = {}
            for choice in ballot.choices:
                candidate_key = choice.candidate.key()
                ballot_dict[candidate_key] = choice.points
            ballots.append(ballot_dict)
        winners = cv.run_cv(ballots, self.slots)
        self.winners = []
        for winner in winners:
            self.winners.append(winner)
        self.result_computed = True
        self.put()

class ElectionPositionCandidate(db.Model):
    """
    A candidate running for an election position.
    """
    election_position = db.ReferenceProperty(ElectionPosition,
                                             required=True,
                                             collection_name='election_position_candidates')
    name = db.StringProperty(required=True)
    written_in = db.BooleanProperty(required=True, default=False)


class RankedBallot(db.Model):
    """
    A single ranked ballot for a ranked voting position.
    """
    position = db.ReferenceProperty(RankedVotingPosition,
                                    required=True,
                                    collection_name='ballots')
    preferences = db.ListProperty(db.Key,
                                  required=True)

class CumulativeVotingBallot(db.Model):
    """
    A single cumulative voting ballot for a cumulate voting position.
    """
    position = db.ReferenceProperty(CumulativeVotingPosition,
                                    required=True,
                                    collection_name='ballots')

class CumulativeVotingChoice(db.Model):
    """
    A single choice within a cumulative voting ballot.
    """
    ballot = db.ReferenceProperty(CumulativeVotingBallot,
                                  required=True,
                                  collection_name='choices')

    candidate = db.ReferenceProperty(ElectionPositionCandidate,
                                     required=True,
                                     collection_name='votes')

    points = db.IntegerProperty(required=True)

class BooleanVotingBallot(db.Model):
    """
    A single boolean ballot for a single boolean position.
    """
    position = db.ReferenceProperty(BooleanVotingPosition,
                                    required=True,
                                    collection_name='ballots')
                                    
class BooleanVotingChoice(db.Model):
    """
    A single choice within a boolean voting ballot.
    """
    ballot = db.ReferenceProperty(BooleanVotingBallot,
                                  required=True,
                                  collection_name='choices')

    candidate = db.ReferenceProperty(ElectionPositionCandidate,
                                     required=True,
                                     collection_name='bool_votes')

    points = db.IntegerProperty(required=True)
    
class Counter(db.Model):
    """
    A simple counter identified by name.
    """
    name = db.StringProperty(required=True)
    count = db.IntegerProperty(required=True, default=0)

    def increment(self, delta=1):
        self.count += delta
        self.put()

class ProcessingJob(db.Model):
    """
    A processing task that runs on the backend using the intern jobs handler"""
    name = db.StringProperty(required=True)
    description = db.StringProperty()
    status = db.StringProperty()
    started = db.DateTimeProperty(required=True, auto_now_add=True)
    ended = db.DateTimeProperty()

    def to_json(self):
        return {
            "key": str(self.key()),
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "started": str(self.started),
            "ended": str(self.ended)
        }

def get_organization(name):
    return Organization.gql("WHERE name=:1", name).get()

def get_all_admins(organization):
    """
    Returns the list of voters who are admins of the specified organization
    """
    return (org_admin.admin.voter for org_admin in 
        OrganizationAdmin.gql("WHERE organization=:1", organization))

def remove_admin(voter, organization):
    admin = Admin.gql("WHERE voter=:1", voter).get()
    if not admin:
        return False
    if organization:
        organization_admin = OrganizationAdmin.gql(
            "WHERE admin=:1 AND organization=:2", admin, organization).get()
        organization_admin.delete()
    admin.delete()

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
    prev_admin = Admin.gql("WHERE voter=:1 AND email=:2", voter, email).get()
    if prev_admin:  # Check if admin entity already exist
        return OrganizationAdmin(admin=prev_admin, organization=organization).put()

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


def delete_election(election):
    """
    Warning: Experimental!
    Deletes the specified election along with all related entities.

    Args:
        election {Election}: the election to delete.
    """
    logging.info('Deleting election: %s', election.name)
    for ev in election.election_voters:
        ev.delete()
    for ep in election.election_positions:
        for epc in ep.election_position_candidates:
            for vote in epc.votes:
                vote.delete()
        for ballot in ep.ballots:
            ballot.delete()
    election.delete()
    logging.info('Election deleted: %s', election.name)


def add_eligible_voters(election, net_id_list):
    """
    Adds the specified people as eligible voters for the election provided. Creates and stores a
    Voter entry for NetIDs who currently do not have a corresponding voter.
    
    Args:
        election: Election object to add eligible voters for.
        net_id_list: List of NetID strings
    """
    logging.info('Adding eligible voters for election %s', election.name)
    num_added = 0
    for net_id in net_id_list:
        if net_id.strip():
            voter = get_voter(net_id.strip(), create=True)
            if voter_status(voter, election) == 'not_eligible':
                ElectionVoter(voter=voter,
                              election=election).put()
                num_added += 1
    logging.info('Added voters; Election: %s, Added: %d, Already Existing: %d',
                 election.name, num_added, len(net_id_list) - num_added)
    election.voter_count += num_added
    election.put()


def remove_eligible_voters(election, net_id_list):
    """
    Removes the specified people from being eligible voters for the election
    provided if they are currently eligible.
    
    Args:
        election: Election object to remove eligible voters for.
        net_id_list: List of NetID strings
    """
    logging.info('Removing eligible voters for election %s', election.name)
    num_removed = 0
    for net_id in net_id_list:
        if net_id.strip():
            voter = get_voter(net_id.strip())
            if not voter:
                continue
            ev = ElectionVoter.gql('WHERE voter=:1 AND election=:2',
                                    voter, election).get()
            if not ev:
                continue
            else:
                ev.delete()
                num_removed += 1
    logging.info('Removed voters; Election: %s, Removed: %d, Not found: %d',
                 election.name, num_removed, len(net_id_list) - num_removed)
    election.voter_count -= num_removed
    election.put()


def update_voter_set(election):
    """
    Updates the cached voter set for an election.
    """
    voter_set = set()
    for ev in election.election_voters:
        voter_set.add(ev.voter.net_id)
    memcache.set(str(election.key())+'-voter-set', voter_set)


def get_voter_set(election):
    """
    Returns the cached voter set for an election.
    """
    voter_set = memcache.get(str(election.key())+'-voter-set')
    if not voter_set:
        update_voter_set(election)
    voter_set = memcache.get(str(election.key())+'-voter-set')
    return voter_set


def get_voter(net_id, create=False):
    """
    Returns the Voter entry for the NetID specified.
    
    Args:
        net_id {String}: NetID of the Voter.
        create {Boolean, optional}: Creates and stores a Voter entry if one doesn't exist.
    
    Returns:
        voter: The Voter entry corresponding to net_id, None if one doesn't exist and create is False.
    """
    voter = Voter.gql('WHERE net_id=:1', net_id).get()
    if not voter and create:    
        voter = Voter(net_id=net_id)
        voter.put()
    return voter


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
    if not election_voter and not election.universal:
        return 'not_eligible'
    elif datetime.now() < election.start or datetime.now() > election.end:
        return 'invalid_time'
    elif not election_voter and election.universal:
        return 'eligible'
    elif election_voter.vote_time:
        return 'voted'
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
        if election.universal:
            election_voter = ElectionVoter(voter=voter, election=election)
        else:
            return False
    election_voter.vote_time = datetime.now()
    election.voted_count += 1
    election.put()
    election_voter.put()
    increment_vote_count()
    return True


def get_vote_count():
    """
    Returns the total number of votes cast on the website.
    """
    name = 'Votes'
    votes_cast = memcache.get('Counter: %s' % name)
    if not votes_cast:
        counter = Counter.gql('WHERE name=:1', name).get()
        if not counter: 
            votes_cast = 0
        else:
            votes_cast = counter.count
        memcache.set('Counter: %s' % name, votes_cast, 9)
    return votes_cast


def increment_vote_count(delta=1):
    """
    Increments the total number of votes cast on the website.

    Args:
        delta {Integer, default=1}: the amount to increment by.
    """
    name = 'Votes'
    counter = Counter.gql('WHERE name=:1', name).get()
    if not counter:
        counter = Counter(name=name)
    counter.increment(delta)
    counter.put()

