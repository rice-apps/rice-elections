import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ManagementModule } from './management/management.module';
import { AdminRoutingModule } from './admin-routing.module';
import { DashboardComponent } from './dashboard/dashboard.component';
import { AdminPageComponent } from './admin.component';

@NgModule({
  imports: [
    CommonModule,
    ManagementModule,
    AdminRoutingModule
  ],
  declarations: [DashboardComponent, AdminPageComponent]
})
export class AdminModule { }
