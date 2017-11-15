import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
// import { OrgProfileComponent } from './org-profile/org-profile.component';
import { OrgElectionComponent } from './org-election/org-election.component';
import { OrgElectionListComponent } from './org-election/org-election-list.component';
import { OrgElectionListItemComponent } from './org-election/org-election-list-item.component';

@NgModule({
  imports: [
    CommonModule
  ],
  declarations: [ OrgElectionComponent, OrgElectionListComponent, OrgElectionListItemComponent]
})
export class OrgAdminDashboardModule { }
