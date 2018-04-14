
import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import {InternalsElection} from "../../../internals/models/internals-election";

@Injectable()
export class ElectionDashService {

  constructor(
    private http: HttpClient
  ) { }

  //get_elections() { }

 get_elections(): Observable<InternalsElection[]> {
    return this.http.get<InternalsElection[]>('/assets/internals-elections.json');
  }

}

