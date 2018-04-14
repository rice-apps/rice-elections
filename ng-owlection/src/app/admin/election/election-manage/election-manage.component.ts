import { Component, Input, OnChanges }       from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import {InternalsElection} from "../../../internals/models/internals-election";
import {ElectionManageService} from "./election-manage.service";
import {Validator} from "@angular/forms";


@Component({
  selector: 'app-election-manage',
  templateUrl: './election-manage.component.html',
  styleUrls: ['./election-manage.component.css']
})
export class ElectionManageComponent implements OnChanges {

  @Input() election: InternalsElection;

  electionForm: FormGroup;
  nameChangeLog: string[] = [];

  constructor(
      private fb: FormBuilder,
      private electionService: ElectionManageService) {

    this.createForm();
    this.logNameChange();
  }

  createForm() {
    this.electionForm = this.fb.group({
        name: '',
        description: '',
        organization: ''
    });
  }

  ngOnChanges() {
    this.rebuildForm();
  }

  rebuildForm() {
    this.electionForm.reset({
        name: this.election.name
    });
  }

  onSubmit() {
    this.election = this.prepareSaveElection();
    this.electionService.updateElections(this.election).subscribe();
    this.rebuildForm()
  }

  prepareSaveElection(): InternalsElection {
    const formModel = this.electionForm.value;

    const saveElection: InternalsElection = {
        id: formModel.name as string,
        name: formModel.name as string,
        description: formModel.description as string,
        organization: formModel.organization as string,
        hidden: false,
        time: Object,
        universal: false,
        status: 'Open',
        results_delay: 0,
        voted_count: 0,
        voter_count: 0
    };
    return saveElection;
  }

  revert() { this.rebuildForm();}

  logNameChange() {
      const nameControl = this.electionForm.get('name');
    nameControl.valueChanges.forEach(
      (value: string) => this.nameChangeLog.push(value)
    );
  }

}