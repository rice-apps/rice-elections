import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {OrgElectionListItemComponent} from "./org-admin-dashboard/org-election/org-election-list-item.component";

const routes: Routes = [
  {path: 'electionslist', component:OrgElectionListItemComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
