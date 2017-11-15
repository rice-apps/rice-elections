import {Component, Input, OnInit} from '@angular/core';
import {orgElectionListItem} from "./org-election-list-item";

@Component({
  selector: 'app-org-election-list-item',
  template: `
    <div>
      <div> {{election.organization}} </div>
      <div> {{election.status}} </div>
      <div> {{election.voter_count}} </div>
      <div> {{election.id}} </div>
      <div> {{election.result_computed}} </div>
      <div> {{election.result_delay}} </div>
      <div> {{election.times.end}} </div>
      <div> {{election.times.start}} </div>s
      <div> {{election.times.pub}} </div>
      <div> {{election.hidden}} </div>
      <div> {{election.name}} </div>
      <div> {{election.universal}} </div>
      <div> {{election.description}} </div>
      <div> {{election.voter_count}} </div>
    </div>
    `
})
export class OrgElectionListItemComponent implements OnInit {


  @Input() election: orgElectionListItem;




  constructor() { }


  ngOnInit() {}

}
