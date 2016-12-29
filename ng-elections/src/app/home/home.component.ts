import { Component, OnInit } from '@angular/core';
import { Http } from '@angular/http';

import 'rxjs/add/operator/toPromise';
import {Organization} from '../shared/models';

const assets = '../../assets';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  organizations: Organization[] = [];
  constructor(private http: Http) {}

  ngOnInit() {
    this.getOganizations()
      .then(orgs => this.organizations = orgs);
  }

  private getOganizations():  Promise<Organization[]> {
    return this.http.get('/api/organizations')
      .toPromise()
      .then(response => response.json().orgs as Organization[])
      .catch(this.handleError);
  }
  private handleError(error: any): Promise<any> {
    console.error(); // for demo purposes only
    return Promise.reject(error.message || error);
  }
}
