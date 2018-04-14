import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';

import { ManagementMembers } from '../model/ManagementMembers';

@Injectable()
export class MembersService {

  constructor(
    private http: HttpClient
  ) { }

  get_members(): Observable<string[]> {
    return this.http.get<string[]>('../assets/members.json');
  }
}
