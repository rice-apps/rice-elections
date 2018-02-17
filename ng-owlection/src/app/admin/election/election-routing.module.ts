import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import {ElectionDashComponent} from "./election-dash/election-dash.component";
import {ElectionManageComponent} from "./election-manage/election-manage.component";
import {InfoComponent} from "./election-manage/info/info.component";
import {PositionsComponent} from "./election-manage/positions/positions.component";
import {VotersComponent} from "./election-manage/voters/voters.component";

export const elecroutes: Routes = [
  {
    path: 'election-dash',
    component: ElectionDashComponent,
  },
  {
    path: 'election-manage',
    component: ElectionManageComponent,
    children: [
      {
        path: 'info',
        component: InfoComponent
      },
      {
        path: 'positions',
        component: PositionsComponent
      },
      {
        path: 'voters',
        component: VotersComponent
      }
    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(elecroutes)],
  exports: [RouterModule]
})
export class ElectionRoutingModule { }
