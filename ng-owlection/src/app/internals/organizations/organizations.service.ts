import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import {InternalsOrganization} from '../models/internals-organization';

@Injectable()
export class OrganizationsService {

  constructor(
    private http: HttpClient
  ) { }

  get_organizations(): Observable<InternalsOrganization[]> {
    return this.http.get<InternalsOrganization[]>('/assets/internals-organizations.json');
  }
}
