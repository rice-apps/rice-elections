import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';

import {AppRoutingModule} from './app-routing.module';
import {AppComponent} from './app.component';
import {AdminModule} from './admin/admin.module';

import { InternalsModule } from './internals/internals.module';
import { ManagementModule } from './admin/management/management.module';

import { BsDropdownModule } from 'ngx-bootstrap/dropdown';
import { ProfileComponent } from './admin/management/profile/profile.component';
import { MembersComponent } from './admin/management/members/members.component';
import { HomeComponent } from './home/home.component';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    // ProfileComponent,
    // MembersComponent
  ],
  imports: [
    BrowserModule,
    BsDropdownModule.forRoot(),
    AdminModule,
    InternalsModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
