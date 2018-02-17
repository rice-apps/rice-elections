import { Injectable } from '@angular/core';
import {Observable} from "rxjs/Observable";
import {HttpClient} from "@angular/common/http";
import {VoterElection} from "./models/voter-elections";

@Injectable()
export class VoterService {

  constructor(
    private http: HttpClient
  ) { }


  getElections(): Observable<Object> {
  return this.http.get('/assets/voter-landing-data.json');
}

  getCurrentElections(): Observable<VoterElection[]> {
    return this.getElections()["open_elections"];
  }

  getFinishedElections(): Observable<VoterElection[]> {
    return this.getElections()["election_results"];
  }

  getElection(id : string): Observable<VoterElection> {

    let filteredCurrentElections = this.getCurrentElections().filter((election, index) => election["id"] == id);
    if (filteredCurrentElections) {
      return filteredCurrentElections[0];
    }

    let filteredFinishedElections = this.getFinishedElections().filter((election, index) => election["id"] == id);
    if (filteredFinishedElections) {
      return filteredFinishedElections[0];
    }

    return;



  }

}
