import { Component, OnInit } from '@angular/core';
import { ProfileService } from '../profile.service';
import { ManagementProfile } from '../../model/ManagementProfile';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit {

  profile: ManagementProfile;

  constructor(
    private profileService: ProfileService
  ) { }

  ngOnInit() {
    this.get_profile();
  }

  get_profile(): void {
    this.profileService.get_profile()
      .subscribe(file => this.profile = file);
  }
}
