import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {HttpClientModule, HttpParams} from '@angular/common/http';

import { AdminRoutingModule } from './admin-routing.module';
import {NgxDatatableModule} from '@swimlane/ngx-datatable';

import { ElectionDashComponent } from './election/election-dash/election-dash.component';
import { ElectionManageComponent } from './election/election-manage/election-manage.component';
import { InfoComponent } from './election/election-manage/info/info.component';
import { PositionsComponent } from './election/election-manage/positions/positions.component';
import { VotersComponent } from './election/election-manage/voters/voters.component';

import {ElectionDashService} from './election/election-dash/election-dash.service';


@NgModule({
  imports: [
    CommonModule,
    AdminRoutingModule,
    HttpClientModule,
    NgxDatatableModule
  ],
  providers: [
    ElectionDashService
  ],
  declarations: [ElectionDashComponent, ElectionManageComponent, InfoComponent, PositionsComponent, VotersComponent]

})
export class AdminModule { }
