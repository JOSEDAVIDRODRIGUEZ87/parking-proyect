import { TestBed } from '@angular/core/testing';

import { ParkingEntryService } from './parking-entry.service';

describe('ParkingEntryService', () => {
  let service: ParkingEntryService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ParkingEntryService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
