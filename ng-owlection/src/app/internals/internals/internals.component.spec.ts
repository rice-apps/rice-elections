import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { InternalsComponent } from './internals.component';

describe('InternalsComponent', () => {
  let component: InternalsComponent;
  let fixture: ComponentFixture<InternalsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ InternalsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(InternalsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
