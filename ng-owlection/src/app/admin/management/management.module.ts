import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ProfileComponent } from './profile/profile.component';
import { MembersComponent } from './members/members.component';
import { ManagementRoutingModule } from './management-routing.module';
import { ProfileService } from './profile.service';

@NgModule({
  imports: [
    ManagementRoutingModule,
    CommonModule
  ],
  exports: [
    ProfileComponent,
    MembersComponent
  ],
  declarations: [ProfileComponent, MembersComponent],
  providers: [ProfileService]
})
export class ManagementModule { }
