import { Component } from '@angular/core';
import {RouterLink} from '@angular/router';

const assets = '../assets';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
    brandlocation = assets + '/shield.png';
}
