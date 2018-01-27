import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import {ProfileComponent} from './profile/profile.component';
import {MemberComponent} from './members/members.component';

const routes: Routes = [
      {
        path: 'profile',
        component: ProfileComponent
      },
      {
        path: 'members'
        component: MemberComponent
      }
    ];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})

export class ManagementRoutingModule { }
