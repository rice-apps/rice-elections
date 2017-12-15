import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import {DashboardComponent} from './dashboard/dashboard.component';
import {ElectionsComponent} from './elections/elections.component';
import {OrganizationsComponent} from './organizations/organizations.component';
import {ReportsComponent} from './reports/reports.component';
import {InternalsComponent} from './internals/internals.component';

const routes: Routes = [
  {
    path: 'intern',
    component: InternalsComponent,
    children: [
      {
        path: '',
        component: DashboardComponent,
        children: [
          {
            path: 'organizations',
            component: OrganizationsComponent
          },
          {
            path: 'elections',
            component: ElectionsComponent
          },
          {
            path: 'reports',
            component: ReportsComponent
          }
        ]
      },

    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class InternalsRoutingModule { }
