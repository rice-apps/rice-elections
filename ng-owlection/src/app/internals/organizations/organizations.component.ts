import {Component, OnInit, TemplateRef, ViewChild} from '@angular/core';
import {OrganizationsService} from './organizations.service';
import {InternalsOrganization} from '../models/internals-organization';
import {Organization} from '../../shared/models/organization';

@Component({
  selector: 'app-organizations',
  templateUrl: './organizations.component.html',
  styleUrls: ['./organizations.component.css']
})
export class OrganizationsComponent implements OnInit {

  organizations: InternalsOrganization[];
  columns = [
    { prop: 'name', name: 'Name', flexGrow: 2 },
    { prop: 'electionCount', name: 'Elections', flexGrow: 1 },
    { prop: 'voteCount', name: 'Votes', flexGrow: 1 },
    { prop: 'adminCount', name: 'Admins', flexGrow: 1 }
  ];

  constructor(
    private orgService: OrganizationsService
  ) { }

  ngOnInit() {
    this.get_all_organizations();
  }

  get_all_organizations(): void {
    this.orgService.get_all_organizations()
      .subscribe(organizations => this.organizations = organizations['organizations']);
  }

  private get_organization(organization: InternalsOrganization): Organization {
    // Parse Organization name
    const org_name = organization.name;

    // setup the response
    let req_org: Organization;
    this.orgService.get_organization(org_name).subscribe((resp) => req_org = resp);
    return req_org;
  }

  getRowHeight(row) {
  // set default
    if (!row) { return 50; }

  // return my height
    return row.height;
  }

  // TODO: Add links into the table to pass on information about what organization admins.
}
