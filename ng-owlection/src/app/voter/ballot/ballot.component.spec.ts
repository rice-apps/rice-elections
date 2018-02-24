import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { BallotComponent } from './ballot.component';

describe('BallotComponent', () => {
  let component: BallotComponent;
  let fixture: ComponentFixture<BallotComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ BallotComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(BallotComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
