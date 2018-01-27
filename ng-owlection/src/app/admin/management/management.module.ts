import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ProfileComponent } from './profile/profile.component';
import { MemberComponent } from './member/member.component';
import { MembersComponent } from './members/members.component';

@NgModule({
  imports: [
    CommonModule
  ],
  declarations: [ProfileComponent, MemberComponent, MembersComponent]
})
export class ManagementModule { }
