import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ElecHomeComponent } from './elec-home/elec-home.component';

import { FormsModule, ReactiveFormsModule }   from '@angular/forms';

@NgModule({
  imports: [
    CommonModule,
    ReactiveFormsModule,
    FormsModule
  ],
  declarations: [ElecHomeComponent]
})
export class ElectionModule { }
