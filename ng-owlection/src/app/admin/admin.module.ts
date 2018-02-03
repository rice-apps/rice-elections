import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ManagementModule } from './management/management.module';
import { AdminRoutingModule } from './admin-routing.module';

@NgModule({
  imports: [
    CommonModule,
    ManagementModule,
    AdminRoutingModule
  ],
  declarations: []
})
export class AdminModule { }
