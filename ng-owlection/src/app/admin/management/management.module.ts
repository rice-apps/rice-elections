import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';
import { ProfileComponent } from './profile/profile.component';
import { MembersComponent } from './members/members.component';
import { ManagementRoutingModule } from './management-routing.module';
import { ProfileService } from './profile.service';
import { MembersService} from './members.service';

@NgModule({
  imports: [
    ManagementRoutingModule,
    CommonModule,
    ReactiveFormsModule
  ],
  exports: [
    ProfileComponent,
    MembersComponent
  ],
  declarations: [ProfileComponent, MembersComponent],
  providers: [ProfileService, MembersService]
})
export class ManagementModule { }
