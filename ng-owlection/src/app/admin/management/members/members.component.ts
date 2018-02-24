import { Component, OnInit } from '@angular/core';
import { MembersService } from '../members.service';
import { ProfileService } from '../profile.service';
import { ManagementMembers } from '../../model/ManagementMembers';

@Component({
  selector: 'app-members',
  templateUrl: './members.component.html',
  styleUrls: ['./members.component.css']
})
export class MembersComponent implements OnInit {

  members: string[];

  constructor(
    private membersService: MembersService
  ) { }

  ngOnInit() {
    this.get_members();
  }

  get_members(): void {
    this.membersService.get_members()
      .subscribe(file => this.members = file["people"]);
  }

}
