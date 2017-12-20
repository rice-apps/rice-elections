import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {InternalsElection} from '../models/internals-election';
import {Observable} from 'rxjs/Observable';

@Injectable()
export class ElectionsService {

  constructor(
    private http: HttpClient
  ) { }

  get_elections(): Observable<InternalsElection[]> {
    return this.http.get<InternalsElection[]>('/assets/internals-elections.json');
  }

}
