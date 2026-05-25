import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { AuthService } from '../../../core/services/auth.service';

@Component({
  selector: 'app-vehicle-list',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './vehicle-list.html',
  styleUrls: ['./vehicle-list.css']
})
export class VehicleList {

  vehicles: any[] = [];
  user: any = null;

  loading = false;
  errorMessage = '';

  constructor(
    private http: HttpClient,
    private authService: AuthService,
    private router: Router
  ) {
    this.user = this.authService.getUser();
  }

  ngOnInit() {
    this.loadVehicles();
  }

  loadVehicles() {

    if (!this.user?.id) {
      this.errorMessage = 'Usuario no autenticado';
      return;
    }

    this.loading = true;

    this.http.get<any[]>(
      `http://localhost:8000/api/vehicles/user/${this.user.id}`
    )
    .subscribe({
      next: (res) => {
        this.vehicles = [...res];
        this.loading = false;
      },
      error: (err) => {
        console.error(err);
        this.errorMessage = 'Error cargando vehículos';
        this.loading = false;
      }
    });
  }

  refresh() {
    this.loadVehicles();
  }

  goToCheckIn(vehicle: any) {

    this.router.navigate(['/parking-entry/entry'], {
      queryParams: {
        vehicle_id: vehicle.id
      }
    });
  }
}