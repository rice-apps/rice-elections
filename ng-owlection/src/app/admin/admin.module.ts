import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';


import { AdminRoutingModule } from './admin-routing.module';

import { ElectionDashComponent } from './election/election-dash/election-dash.component';
import { ElectionManageComponent } from './election/election-manage/election-manage.component';
import {HttpClientModule} from "@angular/common/http";
import {NgxDatatableModule} from "@swimlane/ngx-datatable";
import {ElectionDashService} from "./election/election-dash/election-dash.service";
import {ElectionHomeService} from "./election/elec-home/elec-home.service";
import {ElecHomeComponent} from "./election/elec-home/elec-home.component";
import { ReactiveFormsModule} from "@angular/forms";
import {ElectionManageService} from "./election/election-manage/election-manage.service";


@NgModule({
  imports: [
    CommonModule,
    AdminRoutingModule,
    HttpClientModule,
    NgxDatatableModule,
      ReactiveFormsModule
  ],
  providers: [ElectionDashService, ElectionHomeService, ElectionManageService],
  declarations: [ElecHomeComponent ,ElectionDashComponent, ElectionManageComponent]
})
export class AdminModule { }
