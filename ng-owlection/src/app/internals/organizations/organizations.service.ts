import { Injectable } from '@angular/core';
import {HttpClient, HttpParams} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import {InternalsOrganization} from '../models/internals-organization';
import {Organization} from '../../shared/models/organization';
import {InternalsOrganizationAdmin} from '../models/internals-organization-admin';

@Injectable()
export class OrganizationsService {

  constructor(
    private http: HttpClient
  ) { }

  get_all_organizations(): Observable<InternalsOrganization[]> {
    // Retrieve all the organizations available

    const url = '/intern/command-center';

    return this.http.get<InternalsOrganization[]>(url);
  }

  get_all_organization_admins(organization: Organization): Observable<InternalsOrganizationAdmin[]> {
    // Retrieve all admins from a given organization object

    const url = '/api/intern/org-admin';

    // Request for OrgAdmins searching by name
    return this.http.get<InternalsOrganizationAdmin[]>(url, {
      params: new HttpParams().set('name', organization.name),
    });
  }

  get_organization(org_name: string): Observable<Organization> {
    // Retrieve organization information for a given organization

    const url = '/api/intern/organization'  ;

    return this.http.get<Organization>(url, {
      params: new HttpParams().set('name', org_name)
    });
  }
}
