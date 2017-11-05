import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OrgAdminsComponent } from './org-admins/org-admins.component';
import {AdminsService} from "./org-admins/admins.service";

@NgModule({
  imports: [
    CommonModule
  ],
  providers: [AdminsService],
  declarations: [ OrgAdminsComponent]
})
export class OrgAdminDashboardModule { }
