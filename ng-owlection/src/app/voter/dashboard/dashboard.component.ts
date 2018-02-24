import { Component, OnInit } from '@angular/core';
import {VoterService} from './voter.service';

import {VoterElection} from '../models/voter-elections';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {
  current_elections: VoterElection[];
  finished_elections: VoterElection[];

  constructor(private voteserv: VoterService) {
  }

  ngOnInit() {
    this.getCurrentElections();
    this.getFinishedElections();
  }

  getCurrentElections(): void {
    this.voteserv.getElections().subscribe(
      res => this.current_elections = res['open_elections']
    );
    console.log(this.current_elections);
  }

  getFinishedElections(): void {
    this.voteserv.getFinishedElections().subscribe(
      res => {
        console.log(res);
        this.finished_elections = res;
      }
    );
    console.log(this.finished_elections);
  }

  getRowHeight(row) {
    // set default
    if (!row) {
      return 50;
    }
  }
}
