import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { RankedPositionComponent } from './ranked-position.component';

describe('RankedPositionComponent', () => {
  let component: RankedPositionComponent;
  let fixture: ComponentFixture<RankedPositionComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ RankedPositionComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(RankedPositionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
