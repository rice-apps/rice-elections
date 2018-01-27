import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ElectionDashComponent } from './election-dash.component';

describe('ElectionDashComponent', () => {
  let component: ElectionDashComponent;
  let fixture: ComponentFixture<ElectionDashComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ElectionDashComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ElectionDashComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
