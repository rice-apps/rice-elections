
import { Component, OnInit } from '@angular/core';
import {InternalsElection} from "../../../internals/models/internals-election";
import {ElectionDashService} from "./election-dash.service";

import {USER} from "../../../shared/models/mock-user"



@Component({
  selector: 'app-election-dash',
  templateUrl: './election-dash.component.html',
  styleUrls: ['./election-dash.component.css']
})
export class ElectionDashComponent implements OnInit {

  elections:InternalsElection[];

  user = USER;

  columns = [
    { prop: 'name', name: 'Name', flexGrow: 3 },
    { prop: 'organization', name: 'Organization', flexGrow: 2 },
    { prop: 'status', name: 'Status', flexGrow: 2 },
    // { prop: 'times.end', hidden: true, sort: true },
    { prop: 'voted_count', name: 'Voted', flexGrow: 1 },
    { prop: 'voter_count', name: 'Voters', flexGrow: 1 }
  ];

  constructor(
    private elecDashService: ElectionDashService
  ) { }

  ngOnInit() {
    this.get_elections();
  }

  get_elections(): void {
    this.elecDashService.get_elections()
      .subscribe(elections => this.elections = elections['elections']);
  }

  getRowHeight(row) {
    //set default
    if (!row) { return 50; }

    //return my height
    return row.height;
  }
}

