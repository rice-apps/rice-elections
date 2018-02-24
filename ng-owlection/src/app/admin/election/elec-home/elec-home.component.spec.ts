import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ElecHomeComponent } from './elec-home.component';

describe('ElecHomeComponent', () => {
  let component: ElecHomeComponent;
  let fixture: ComponentFixture<ElecHomeComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ElecHomeComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ElecHomeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
