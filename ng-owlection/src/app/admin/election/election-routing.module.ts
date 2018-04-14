import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import {ElectionDashComponent} from "./election-dash/election-dash.component";
import {ElectionManageComponent} from "./election-manage/election-manage.component";

export const elecroutes: Routes = [
  {
    path: 'election-dash',
    component: ElectionDashComponent,
  },
  {
    path: 'election-manage',
    component: ElectionManageComponent
  }
];

@NgModule({
  imports: [RouterModule.forChild(elecroutes)],
  exports: [RouterModule]
})
export class ElectionRoutingModule { }
