import { Component, OnInit } from '@angular/core';
import {InternalsElection} from '../models/internals-election';
import {ElectionsService} from './elections.service';

@Component({
  selector: 'app-elections',
  templateUrl: './elections.component.html',
  styleUrls: ['./elections.component.css']
})
export class ElectionsComponent implements OnInit {

  elections: InternalsElection[];
  columns = [
    { prop: 'name', name: 'Name', flexGrow: 3 },
    { prop: 'organization', name: 'Organization', flexGrow: 2 },
    { prop: 'status', name: 'Status', flexGrow: 2 },
    // { prop: 'times.end', hidden: true, sort: true },
    { prop: 'voted_count', name: 'Voted', flexGrow: 1 },
    { prop: 'voter_count', name: 'Voters', flexGrow: 1 }
  ];

  constructor(
    private elecService: ElectionsService
  ) { }

  ngOnInit() {
    this.get_elections();
  }

  get_elections(): void {
    this.elecService.get_elections()
      .subscribe(elections => console.log(elections)); // this.elections = elections['elections']);
  }

  getRowHeight(row) {
  // set default
    if (!row) { return 50; }

  // return my height
    return row.height;
}
}
