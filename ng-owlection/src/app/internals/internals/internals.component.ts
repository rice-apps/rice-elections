import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-internals',
  template: `
    <router-outlet></router-outlet>
  `,
  styles: []
})
export class InternalsComponent implements OnInit {

  constructor() { }

  ngOnInit() {
  }

}
