import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import {elecroutes} from "./election/election-routing.module";
import {ElectionDashComponent} from "./election/election-dash/election-dash.component";
import {ElecHomeComponent} from "./election/elec-home/elec-home.component";

const routes: Routes = [
  {path: 'admin',
  children: [
    {
      path: '',
      component: ElecHomeComponent,
      children: elecroutes
    }
  ]}
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AdminRoutingModule { }
