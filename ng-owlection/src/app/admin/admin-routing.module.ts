import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { ProfileComponent } from './management/profile/profile.component';

const routes: Routes = [
  {
    path: 'admin',
    component: ProfileComponent // TODO: will change to DashboardComponent later
  },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AdminRoutingModule { }
