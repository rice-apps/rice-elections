import { Component, OnInit } from '@angular/core';
import {ElectionHomeService} from "./elec-home.service";

@Component({
  selector: 'app-elec-home',
  templateUrl: './elec-home.component.html',
  styleUrls: ['./elec-home.component.css']
})
export class ElecHomeComponent implements OnInit {

  constructor(
    private elecHomeService: ElectionHomeService
  ) { }

  ngOnInit() {
  }

}
