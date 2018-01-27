import { TestBed, inject } from '@angular/core/testing';

import { ElectionDashService } from './election-dash.service';

describe('ElectionDashService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [ElectionDashService]
    });
  });

  it('should be created', inject([ElectionDashService], (service: ElectionDashService) => {
    expect(service).toBeTruthy();
  }));
});
