import { Injectable } from '@angular/core';
import {HttpClient, HttpParams} from '@angular/common/http';
import {InternalsElection } from '../../../internals/models/internals-election';
import {Observable} from 'rxjs/Observable';

@Injectable()
export class ElectionDashService {

  constructor(
    private http: HttpClient
  ) { }

  get_elections() {
    return this.http.get<InternalsElection[]>('/assets/internals-elections.json');
  }

  filter_elections() {
     //return this.http.get<InternalsElection[]>('/assets/internals-elections.json', {params: new HttpParams().set("organization", "Jones College")});
     // user Pipe to filter JSON
  }

}

