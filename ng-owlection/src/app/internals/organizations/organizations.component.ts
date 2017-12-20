import {Component, OnInit, TemplateRef, ViewChild} from '@angular/core';
import {OrganizationsService} from './organizations.service';
import {InternalsOrganization} from '../models/internals-organization';

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
    this.get_organizations();
  }

  get_organizations(): void {
    this.orgService.get_organizations()
      .subscribe(organizations => this.organizations = organizations['organizations']);
  }

  getRowHeight(row) {
  // set default
    if (!row) { return 50; }

  // return my height
    return row.height;
}
}
