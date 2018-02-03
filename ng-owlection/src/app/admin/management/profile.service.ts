import { Injectable } from '@angular/core';

@Injectable()
export class ProfileService {

  constructor(
    private http: HttpClient
  ) { }

  get_elections(): Observable<InternalsElection[]> {
    return this.http.get<InternalsElection[]>('/assets/organization-admin-page-data.json');
  }
}
