import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { VoterRoutingModule } from './voter-routing.module';
import { DashboardComponent } from './dashboard/dashboard.component';
import { BallotComponent } from './ballot/ballot.component';
import { ResultsComponent } from './results/results.component';
import {VoterService} from './dashboard/voter.service';
import {NgxDatatableModule} from '@swimlane/ngx-datatable';

@NgModule({
  imports: [
    CommonModule,
    NgxDatatableModule,
    VoterRoutingModule
  ],
  providers: [VoterService],
  declarations: [DashboardComponent, BallotComponent, ResultsComponent]
})
export class VoterModule { }
