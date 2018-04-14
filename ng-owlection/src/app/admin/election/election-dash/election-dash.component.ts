
import { Component, OnInit } from '@angular/core';
import {InternalsElection} from "../../../internals/models/internals-election";
import {ElectionDashService} from "./election-dash.service";

import {USER} from "../../../shared/models/mock-user";
import { Router, NavigationExtras } from "@angular/router";


@Component({
  selector: 'app-election-dash',
  templateUrl: './election-dash.component.html',
  styleUrls: ['./election-dash.component.css']
})
export class ElectionDashComponent implements OnInit {

  elections:InternalsElection[];

  user = USER;
  organization = "Jones College";
  selected = []


  columns = [
    { prop: 'name', name: 'Name', flexGrow: 3 },
    { prop: 'organization', name: 'Organization', flexGrow: 2 },
    { prop: 'status', name: 'Status', flexGrow: 2 },
    { prop: 'voted_count', name: 'Voted', flexGrow: 1 },
    { prop: 'voter_count', name: 'Voters', flexGrow: 1 }
  ];

  constructor(
     private elecDashService: ElectionDashService, private rtr: Router
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

  onSelect({ selected }) {
    console.log("Select Event", selected, this.selected[0]["id"]);
    this.rtr.navigate(["/admin/election-manage"], { queryParams: { id: this.selected[0]["id"]} });



  }
}

