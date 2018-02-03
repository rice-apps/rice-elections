import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import {ProfileComponent} from './profile/profile.component';
import {MembersComponent} from './members/members.component';

const routes: Routes = [
      {
        path: 'profile',
        component: ProfileComponent
      },
      {
        path: 'members',
        component: MembersComponent
      }
    ];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})

export class ManagementRoutingModule { }
