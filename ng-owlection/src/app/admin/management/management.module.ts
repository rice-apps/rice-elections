import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ProfileComponent } from './profile/profile.component';
import { MembersComponent } from './members/members.component';
import { ManagementRoutingModule } from './management-routing.module';

@NgModule({
  imports: [
    ManagementRoutingModule,
    CommonModule
  ],
  exports: [
    ProfileComponent,
    MembersComponent
  ],
  declarations: [ProfileComponent, MembersComponent]
})
export class ManagementModule { }
