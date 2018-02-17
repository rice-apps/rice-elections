import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ManagementModule } from './management/management.module';
import { AdminRoutingModule } from './admin-routing.module';
import { DashboardComponent } from './dashboard/dashboard.component';

@NgModule({
  imports: [
    CommonModule,
    ManagementModule,
    AdminRoutingModule
  ],
  declarations: [DashboardComponent]
})
export class AdminModule { }
