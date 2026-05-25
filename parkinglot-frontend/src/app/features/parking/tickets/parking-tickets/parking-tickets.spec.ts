import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ParkingTickets } from './parking-tickets';

describe('ParkingTickets', () => {
  let component: ParkingTickets;
  let fixture: ComponentFixture<ParkingTickets>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ParkingTickets],
    }).compileComponents();

    fixture = TestBed.createComponent(ParkingTickets);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
