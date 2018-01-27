import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ElectionManageComponent } from './election-manage.component';

describe('ElectionManageComponent', () => {
  let component: ElectionManageComponent;
  let fixture: ComponentFixture<ElectionManageComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ElectionManageComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ElectionManageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
