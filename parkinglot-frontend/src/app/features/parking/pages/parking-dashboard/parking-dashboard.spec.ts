import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ParkingDashboard } from './parking-dashboard';

describe('ParkingDashboard', () => {
  let component: ParkingDashboard;
  let fixture: ComponentFixture<ParkingDashboard>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ParkingDashboard],
    }).compileComponents();

    fixture = TestBed.createComponent(ParkingDashboard);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
