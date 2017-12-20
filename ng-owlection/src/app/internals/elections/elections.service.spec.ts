import { TestBed, inject } from '@angular/core/testing';

import { ElectionsService } from './elections.service';

describe('ElectionsService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [ElectionsService]
    });
  });

  it('should be created', inject([ElectionsService], (service: ElectionsService) => {
    expect(service).toBeTruthy();
  }));
});
