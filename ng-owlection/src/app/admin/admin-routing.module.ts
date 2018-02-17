import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {ElectionDashComponent} from "./election/election-dash/election-dash.component";
import {ElectionManageComponent} from "./election/election-manage/election-manage.component";
import {InfoComponent} from "./election/election-manage/info/info.component";
import {PositionsComponent} from "./election/election-manage/positions/positions.component";
import {VotersComponent} from "./election/election-manage/voters/voters.component";

const routes: Routes = [
  {
    path: 'election-dash',
    component: ElectionDashComponent,
  },
  {
    path: 'election-manage',
    component: ElectionManageComponent,
    children: [
      {
        path: '',
        component: ElectionManageComponent
      },
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
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AdminRoutingModule { }
