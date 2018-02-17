import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';

import { InternalsElection } from '../../internals/models/internals-election';

@Injectable()
export class ProfileService {

  constructor(
    private http: HttpClient
  ) { }

  get_elections(): Observable<InternalsElection[]> {
    return this.http.get<InternalsElection[]>('/assets/organization-admin-page-data.json');
  }
}
