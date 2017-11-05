import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { OrgElectionComponent } from './org-election.component';

describe('OrgElectionComponent', () => {
  let component: OrgElectionComponent;
  let fixture: ComponentFixture<OrgElectionComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ OrgElectionComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(OrgElectionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
