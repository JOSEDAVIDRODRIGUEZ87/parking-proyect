import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ParkingExit } from './parking-exit';

describe('ParkingExit', () => {
  let component: ParkingExit;
  let fixture: ComponentFixture<ParkingExit>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ParkingExit],
    }).compileComponents();

    fixture = TestBed.createComponent(ParkingExit);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
