import { Component, OnInit, Input } from '@angular/core';
import {InternalsElection} from "../../../internals/models/internals-election";

import {ElectionManageService} from "./election-manage.service";

import { ActivatedRoute, Router } from "@angular/router";

import {Observable} from 'rxjs/Observable';
import {FormBuilder, FormControl, FormGroup} from '@angular/forms';
//import {ElectionDashService} from "../election-dash/election-dash.service";

@Component({
  selector: 'app-election-manage',
  templateUrl: './election-manage.component.html',
  styleUrls: ['./election-manage.component.css']
})
export class ElectionManageComponent implements OnInit {

  formId = "";
  name = "name";
  election: InternalsElection;




  /*def_date = new Date();
  election: InternalsElection={
    id: "yay",
    name: "name",
    description: "description",
    organization: "organization",
    hidden: true,
    universal: true,
    times: this.def_date,
    status: "status",
    results_delay: 1,
    voted_count: 1,
    voter_count: 1,
  }; */

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private elecManageService: ElectionManageService,
    private fb: FormBuilder
  ) {
    this.createForm();

  }

  ngOnInit() {
    this.formId = this.route.snapshot.queryParams["id"];
    this.get_election(this.formId);
    //this.populateForm(this.election);

  }

  /*onSubmit(number){
    console.log("Number: " + number);
  } */
  onSubmit(){
    console.log("Submitted");
  }

  get_election(id): void {

      this.elecManageService.get_election(id).subscribe(elections => this.election = elections["election"]);

     console.log("Next is the election!");
     console.log(this.election);

  }

  dummy = new FormControl();

  electionForm: FormGroup;
  createForm(){
    this.electionForm = this.fb.group({
      title: '', // <--- the FormControl called "name"
    });
  }

  populateForm(InternalsElection): InternalsElection {
    return null;
  }



}


/*
* @Input() election: InternalsElection[];
  def_date = new Date();
  // def_date = new Date(2000, 1, 1, 0, 0, 0);

  model: InternalsElection = {
    id: "",
    name: "New Election",
    description: "Description",
    organization: "xyz",
    hidden: false,
    universal: false,
    times: this.def_date,
    status: "Closed",
    results_delay: 0,
    voted_count: 0,
    voter_count: 0
  }

  submitted = false;

  onSubmit() {this.submitted = true;}
*
* */
