import { Component, OnInit } from '@angular/core';
import {AdminsService} from "./admins.service";

@Component({
  selector: 'app-org-admins',
  templateUrl: './org-admins.component.html',
  styleUrls: ['./org-admins.component.css']
})
export class OrgAdminsComponent implements OnInit {
  admins: string[];

  constructor(private adminsService : AdminsService) {}
  getAdmins(): void {
    this.adminsService.getAdmins().then(admins => this.admins = admins);
  }

  ngOnInit(): void {
    this.getAdmins();
  }

}
