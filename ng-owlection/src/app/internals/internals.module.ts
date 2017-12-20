import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {HttpClientModule} from '@angular/common/http';

import { InternalsRoutingModule } from './internals-routing.module';
import {NgxDatatableModule} from '@swimlane/ngx-datatable';

import { DashboardComponent } from './dashboard/dashboard.component';
import { OrganizationsComponent } from './organizations/organizations.component';
import { ElectionsComponent } from './elections/elections.component';
import { ReportsComponent } from './reports/reports.component';
import { InternalsComponent } from './internals/internals.component';

import {OrganizationsService} from './organizations/organizations.service';
import {DashboardService} from './dashboard/dashboard.service';
import {ElectionsService} from './elections/elections.service';

@NgModule({
  imports: [
    CommonModule,
    InternalsRoutingModule,
    HttpClientModule,
    NgxDatatableModule
  ],
  providers: [
    DashboardService,
    OrganizationsService,
    ElectionsService
  ],
  declarations: [DashboardComponent, OrganizationsComponent, ElectionsComponent, ReportsComponent, InternalsComponent]
})
export class InternalsModule { }
