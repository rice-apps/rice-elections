import { Injectable } from '@angular/core';

import { HttpClient } from '@angular/common/http';

import { InternalsOrganization } from '../models/internals-organization';
import { Observable } from 'rxjs/Observable';

@Injectable()
export class DashboardService {

  constructor(
    private http: HttpClient
  ) { }
}
