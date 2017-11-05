import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { OrgElectionListItemComponent } from './org-election-list-item.component';

describe('OrgElectionListItemComponent', () => {
  let component: OrgElectionListItemComponent;
  let fixture: ComponentFixture<OrgElectionListItemComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ OrgElectionListItemComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(OrgElectionListItemComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
