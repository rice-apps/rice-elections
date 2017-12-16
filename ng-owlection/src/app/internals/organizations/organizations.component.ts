import {Component, OnInit, TemplateRef, ViewChild} from '@angular/core';
import {OrganizationsService} from './organizations.service';
import {InternalsOrganization} from '../models/organization';

@Component({
  selector: 'app-organizations',
  templateUrl: './organizations.component.html',
  styleUrls: ['./organizations.component.css']
})
export class OrganizationsComponent implements OnInit {

  organizations: InternalsOrganization[];
  columns = [
    { prop: 'name', name: 'Name' },
    { prop: 'electionCount', name: 'Elections' },
    { prop: 'voteCount', name: 'Votes' },
    { prop: 'adminCount', name: 'Admins' }
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
}
