import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { ProfileComponent } from './management/profile/profile.component';
import { MembersComponent } from './management/members/members.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { AdminPageComponent } from './admin.component';

const routes: Routes = [
  {
    path: 'admin',
    component: AdminPageComponent,
    children : [
      { path: '',
        component: DashboardComponent,
        children: [
          {
            path: 'profile',
            component: ProfileComponent
          },
          {
            path: 'members',
            component: MembersComponent
          }
        ]
      }
    ]
  },
];



@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AdminRoutingModule { }
