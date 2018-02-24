
import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';

@Injectable()
export class ElectionHomeService {

  constructor(
    private http: HttpClient
  ) { }

  get_elections() { }

}
