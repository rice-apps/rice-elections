import { Component, OnInit } from '@angular/core';

const assets = '../../assets';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  organizations = [
    {'name': 'Architectural Society', 'imgsrc': assets + '/who/architectural-society-rice.png'},
    {'name': 'Baker College', 'imgsrc': assets + '/who/baker-college.gif'},
    {'name': 'Brown College', 'imgsrc': assets + '/who/brown-college.png'},
    {'name': 'Chi Epsilon', 'imgsrc': assets + '/who/chi-epsilon.jpg'},
    {'name': 'Chinese Student Association', 'imgsrc': assets + '/who/chinese-student-association.jpg'}
  ];

  constructor() { }

  ngOnInit() {
  }

}
