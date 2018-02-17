import { Injectable } from '@angular/core';

import {HttpClient} from '@angular/common/http';

@Injectable()
export class ElectionService {

  constructor(
    private http: HttpClient
  ) { }
}
