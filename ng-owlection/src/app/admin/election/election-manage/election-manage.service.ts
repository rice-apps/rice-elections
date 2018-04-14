import { Injectable } from '@angular/core';
import {HttpClient, HttpErrorResponse, HttpParams} from '@angular/common/http';
import {InternalsElection } from '../../../internals/models/internals-election';

import {Observable} from 'rxjs/Observable';

import 'rxjs/add/operator/catch'; // don't forget this, or you'll get a runtime error

@Injectable()
export class ElectionManageService {

  def_date = new Date();
  model: InternalsElection={
    id: "yay",
    name: "name",
    description: "description",
    organization: "organization",
    hidden: true,
    universal: true,
    times: this.def_date,
    status: "status",
    results_delay: 1,
    voted_count: 1,
    voter_count: 1,
  };

  constructor(
    private http: HttpClient
  ) { }

  //formerly get_election(): Observable<InternalsElection> {}
  get_election(id): Observable<InternalsElection> {

    const options = id ? { params: new HttpParams().set('id', id) } : {};
    return this.http.get<InternalsElection>('/api/organizations', options);


    //return this.model;
    //return this.http.get<InternalsElection[]>('/assets/internals-elections.json');

    // this doesn't work: return this.http.get<InternalsElection>('/api/organizations')
    //       .catch(function(err: HttpErrorResponse) {
    //         console.error('An error occurred:', err.error);
    //         return Observable.of("Hi");
    //       });
  }

}
