import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {ElectionDashComponent} from "./election/election-dash/election-dash.component";
import {ElectionManageComponent} from "./election/election-manage/election-manage.component";
import {InfoComponent} from "./election/election-manage/info/info.component";
import {PositionsComponent} from "./election/election-manage/positions/positions.component";
import {VotersComponent} from "./election/election-manage/voters/voters.component";


import { elecroutes } from './election/election-routing.module'


const routes: Routes = [
 {
 path: 'admin',
 children: elecroutes
 }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AdminRoutingModule { }
