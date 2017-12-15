import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { InternalsRoutingModule } from './internals-routing.module';

import { DashboardComponent } from './dashboard/dashboard.component';
import { OrganizationsComponent } from './organizations/organizations.component';
import { ElectionsComponent } from './elections/elections.component';
import { ReportsComponent } from './reports/reports.component';
import { InternalsComponent } from './internals/internals.component';

@NgModule({
  imports: [
    CommonModule,
    InternalsRoutingModule
  ],
  declarations: [DashboardComponent, OrganizationsComponent, ElectionsComponent, ReportsComponent, InternalsComponent]
})
export class InternalsModule { }
