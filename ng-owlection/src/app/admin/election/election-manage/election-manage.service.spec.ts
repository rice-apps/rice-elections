import { TestBed, inject } from '@angular/core/testing';

import { ElectionManageService } from './election-manage.service';

describe('ElectionManageService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [ElectionManageService]
    });
  });

  it('should be created', inject([ElectionManageService], (service: ElectionManageService) => {
    expect(service).toBeTruthy();
  }));
});
