import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { OrgElectionListComponent } from './org-election-list.component';

describe('OrgElectionListComponent', () => {
  let component: OrgElectionListComponent;
  let fixture: ComponentFixture<OrgElectionListComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ OrgElectionListComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(OrgElectionListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
