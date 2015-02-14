"""
Run once, be happy forever. (Only once!)
If this ends up on Github...
"""

from models import models

def main():
    print "Creating organizations..."

    brown = models.Organization(name='Brown College',
                                description='The best residential college.',
                                image='/static/img/who/brown-college.png',
                                website='http://brown.rice.edu')
    brown.put()
    mcmurtry = models.Organization(name='McMurtry College',
                                description='Not the best residential college.',
                                image='/static/img/who/mcmurtry-college.png',
                                website='http://mcmurtry.rice.edu')
    mcmurtry.put()
    baker = models.Organization(name='Baker College',
                                description='Not the best residential college.',
                                image='/static/img/who/mcmurtry-college.png',
                                carousel_show_name=False,
                                website='http://baker.rice.edu')
    baker.put()
    martel = models.Organization(name='Martel College',
                                description='Best deck.',
                                website='http://martel.rice.edu')
    martel.put()

    testing = models.Organization(name='Testing',
                                  description='Test 1 2 3',
                                  website='foo.bar')
    testing.put()

    print "Done."
    print "Creating admins..."

    users = [
        ('wa1', 'wa1@rice.edu'),
        ('dan1', 'dan1@rice.edu'),
        ('jcc7', 'jcc7@rice.edu'),
        ('jbb4', 'jbb4@rice.edu'),
        ('cmp1', 'cmp1@rice.edu'),
        ('pe4', 'pe4@rice.edu'),
        ('wcl2', 'wcl2@rice.edu')
    ]

    admins = []

    for net_id, email in users:
        voter = models.get_voter(net_id, create=True)
        admin = models.Admin(voter=voter, email=email).put()
        admins.append(admin)


    for admin in admins[:3]:
        models.OrganizationAdmin(admin=admin, organization=brown).put()

    models.OrganizationAdmin(admin=admins[3], organization=mcmurtry).put()
    models.OrganizationAdmin(admin=admins[4], organization=baker).put()
    models.OrganizationAdmin(admin=admins[5], organization=martel).put()
    models.OrganizationAdmin(admin=admins[6], organization=testing).put()

    print "Done."

if __name__ == '__main__':
    main()
