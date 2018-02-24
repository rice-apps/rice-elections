import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';

import { ManagementMembers } from '../model/ManagementMembers';

@Injectable()
export class MembersService {

  constructor(
    private http: HttpClient
  ) { }

  get_members(): Observable<ManagementMembers> {
    return this.http.get<ManagementMembers>('/assets/members.json');
  }
}
