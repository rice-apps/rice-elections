import { Component, ViewChild, OnInit } from '@angular/core';
import { ProfileService } from '../profile.service';
import { ManagementProfile } from '../../model/ManagementProfile';

import { FormBuilder, FormGroup } from '@angular/forms';
// import { FormsModule, ReactiveFormsModule } from '@angular/forms';


@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit {

  @ViewChild("fileInput") fileInput;

  profile: ManagementProfile;

  profileForm: FormGroup;

  edit = '';

  constructor(
    private profileService: ProfileService,
    private profilefb: FormBuilder
  ) {
    this.create_form();
  }

  ngOnInit() {
    this.get_profile();
  }

  get_profile(): void {
    this.profileService.get_profile()
      .subscribe(file => {
        this.profile = file;
        this.profileForm.setValue({
          name: this.profile.name,
          website: this.profile.website,
          description: this.profile.description
        })
    })
  }
  //
  // add_file(): void {
  //   let fi = this.fileInput.nativeElement;
  //   if (fi.files && fi.files[0]) {
  //       let fileToUpload = fi.files[0];
  //       this.uploadService
  //           .upload(fileToUpload)
  //           .subscribe(res => {
  //               console.log(res);
  //           });
  //   }
  // }

  create_form() {
    this.profileForm = this.profilefb.group({
      name: '', // <--- the FormControl called "name"
      website: '',
      description: ''
    });
  }

  editName(name: String) {
    if (name) {
      this.profileForm.patchValue({
        name: name;
      })
      this.profile.name = name;
    }
  }

  editWebsite(website: String) {
    if (website) {
      this.profileForm.patchValue({
        website: website;
      })
      this.profile.website = website;
    }
  }

  editDescription(description: String) {
    if (description) {
      this.profileForm.patchValue({
        description: description;
      })
      this.profile.description = description;
    }
  }

  // ngOnChanges() { // <-- call rebuildForm in ngOnChanges
  //   this.rebuildForm();
  // }
  //
  // rebuildForm() { // <-- wrap patchValue in rebuildForm
  //   this.profileForm.reset();
  //   this.profileForm.patchValue({
  //     name: this.profile.name,
  //     website: this.profile.website,
  //     description: this.profile.description
  //   });
  // }

}
