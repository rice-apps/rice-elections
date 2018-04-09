import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

import {RankedPosition} from "./ranked-position";

@Component({
  selector: 'app-ranked-position',
  templateUrl: './ranked-position.component.html',
  styleUrls: ['./ranked-position.component.css']
})
export class RankedPositionComponent implements OnInit {
  rankedPositionForm: FormGroup;

  constructor(private fb: FormBuilder) {
    this.createForm();
  }

  createForm() {
    this.rankedPositionForm = this.fb.group({
      rankedPosition: this.fb.group(new RankedPosition())
    });
  }

  ngOnInit() {
  }

}
