import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { OrgAdminsComponent } from './org-admins.component';

describe('OrgAdminsComponent', () => {
  let component: OrgAdminsComponent;
  let fixture: ComponentFixture<OrgAdminsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ OrgAdminsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(OrgAdminsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
