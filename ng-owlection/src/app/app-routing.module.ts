import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {OrgAdminsComponent} from "./org-admin-dashboard/org-admins/org-admins.component";

const routes: Routes = [
  {
    path: 'admins',
    component: OrgAdminsComponent
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
