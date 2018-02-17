import { TestBed, inject } from '@angular/core/testing';

import { ViewResultsService } from './view-results.service';

describe('ViewResultsService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [ViewResultsService]
    });
  });

  it('should be created', inject([ViewResultsService], (service: ViewResultsService) => {
    expect(service).toBeTruthy();
  }));
});
