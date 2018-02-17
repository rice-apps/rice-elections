import { TestBed, inject } from '@angular/core/testing';

import { CastBallotService } from './cast-ballot.service';

describe('CastBallotService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [CastBallotService]
    });
  });

  it('should be created', inject([CastBallotService], (service: CastBallotService) => {
    expect(service).toBeTruthy();
  }));
});
