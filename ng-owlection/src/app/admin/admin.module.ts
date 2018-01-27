import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { AdminRoutingModule } from './admin-routing.module';
import { ElectionDashComponent } from './election-dash/election-dash.component';
import { ElectionManageComponent } from './election-manage/election-manage.component';
import { InfoComponent } from './election-manage/info/info.component';
import { PositionsComponent } from './election-manage/positions/positions.component';
import { VotersComponent } from './election-manage/voters/voters.component';

@NgModule({
  imports: [
    CommonModule,
    AdminRoutingModule
  ],
  declarations: [ElectionDashComponent, ElectionManageComponent, InfoComponent, PositionsComponent, VotersComponent]
})
export class AdminModule { }
