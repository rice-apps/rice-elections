"""
Controller for website administration stuff.
"""

import datetime
import json
import logging
import sys
import webapp2
from time import sleep

from authentication import auth
from google.appengine.ext import deferred
from models import models, webapputils, report_results, new_results
from google.appengine.api import mail, taskqueue

COMMANDERS = ['wa1', 'wcl2', 'stl2']

class CommandCenterHandler(webapp2.RequestHandler):

    def get(self):
        voter = auth.get_voter(self)
        if voter.net_id not in COMMANDERS:
            return webapputils.render_page(self, '/templates/message', {
                'status': 'Not Authorized',
                'msg': "You're not authorized to enter the command center"
            })

        organizations = []
        # Aggregate all information about organizations
        for org in models.Organization.all():
            organizations.append({
                'name': org.name,
                'electionCount': org.elections.count(),
                'adminCount': org.organization_admins.count(),
                'voteCount': sum([elec.voted_count for elec in org.elections])
            })


        # get 20 elections that have not ended, sorted by starting time
        elections = [e.to_json(True) for e in 
            models.Election.all().order('-end').order('start').run(limit=20)]
        page_data = {
            "organizations": organizations,
            "elections": elections
        }
        return webapputils.render_page(self, '/intern/command-center', page_data)

    def post(self):
        methods = {
            'create_organization': self.create_organization,
            'add_admin': self.add_admin
        }
        data = json.loads(self.request.get('data'))
        voter = auth.get_voter(self)
        if voter.net_id not in COMMANDERS:
            return  # hacker
        out = methods[data['method']](data)

    def create_organization(self, data):
        org = models.Organization(
            name=data['name'],
            description=data['description'],
            website=data['website']
        )
        org.put()
        webapputils.respond(self, 'OK', 'Done')

    def add_admin(self, data):
        org = models.Organization.get(data['organization'])
        voter = get_voter(data['net_id'], create=True)
        org_admin = models.put_admin(voter, data['email'], org)
        if org_admin:
            webapputils.respond(self, 'OK', 'Done')
        else:
            webapputils.respond(self, 'ERROR', "Couldn't create admin")

class JobsHandler(webapp2.RequestHandler):
    """Large processing tasks that should be executed on the server side, instead
    of the remote api shell for performance and cost reasons. If you are running
    a task on the remote api shell that will load thousands of Datastore objects
    it will be extremely slow and very expensive so write the code here instead
    and run it on the server by accessing the endpoint ONCE."""

    def get(self):
        voter = auth.get_voter(self)
        if voter.net_id not in COMMANDERS:
            return webapputils.render_page(self, '/templates/message', {
                'status': 'Not Authorized',
                'msg': "You're not authorized to enter the command center"
            })

        jobs = models.ProcessingJob.gql("ORDER BY started DESC LIMIT 20")
        ready = {
            "name": "WillRiceSpringRound3Unsent2",
            "description": "Send out updated email"
        }

        page_data = {
            "jobs": jobs,
            "ready": ready
        }

        return webapputils.render_page(self, '/intern/jobs', page_data)

    def post(self):

        job = models.ProcessingJob(
            name=self.request.get('ready_name'),
            description=self.request.get('ready_description'),
            status='running'
        )

        job.put()

        retry_options = taskqueue.TaskRetryOptions(task_retry_limit=0)
        taskqueue.add(
            name=job.name,
            url='/intern/jobs-taskqueue',
            params={
                'job_key': str(job.key())
            },
            retry_options=retry_options,
            target='task-manager',
            queue_name='voters'
        )

        self.response.write(json.dumps(job.to_json()))


class JobsTaskQueueHandler(webapp2.RequestHandler):

    def post(self):
        job = models.ProcessingJob.get(self.request.get('job_key'))

        try:
            description = "Send out updated email"
            # Assertion here to ensure that the developer is running the right
            # task
            assert(job.description == description)


            ### Processing begin ###
            jones_c = models.Organization.gql("WHERE name='Baker College'").get()
            wrc_election = models.Election.get_by_id(6550983727382528)

            for pos in wrc_election.election_positions:
                pos.compute_winners()
            gen_election = models.Election.gql("WHERE name='General Election 2016'").get()

            admin_emails = [admin.admin.email for admin in models.OrganizationAdmin.gql("WHERE organization=:1", jones_c).fetch(None)]
            admin_emails.append(u'stl2@rice.edu')
            deferred.defer(new_results.email_election_results, admin_emails, wrc_election, _queue='election-results')

            # for pos in gen_election.election_positions:
            #     new_results.email_election_results(['stl2@rice.edu'], gen_election, pos)
            ### Processing end ###

            job.status = "complete"
        finally:
            if job.status != "complete":
                job.status = "failed"
            job.ended = datetime.datetime.now()
            job.put()


app = webapp2.WSGIApplication([
    ('/intern/command-center', CommandCenterHandler),
    ('/intern/jobs', JobsHandler),
    ('/intern/jobs-taskqueue', JobsTaskQueueHandler)
], debug=True)
