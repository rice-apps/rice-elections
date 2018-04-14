import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';

import { ManagementProfile } from '../model/ManagementProfile';

@Injectable()
export class ProfileService {

  constructor(
    private http: HttpClient
  ) { }

  get_profile(): Observable<ManagementProfile> {
    return this.http.get<ManagementProfile>('../../../assets/Management-Profile.json');
  }

  upload(fileToUpload: any) {
    let input = new FormData();
    input.append("file", fileToUpload);

    return this.http
        .post("/api/uploadFile", input);
  }
}
