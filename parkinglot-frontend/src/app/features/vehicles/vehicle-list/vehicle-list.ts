import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { AuthService } from '../../../core/services/auth.service';

@Component({
  selector: 'app-vehicle-list',
  standalone: true,
  imports: [], // 🔧 Removido CommonModule ya que usas el nuevo control de flujo (@if, @for)
  templateUrl: './vehicle-list.html',
  styleUrls: ['./vehicle-list.css']
})
export class VehicleList implements OnInit { // 🔧 Añadido implements OnInit

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

  ngOnInit(): void {
    this.loadVehicles();
  }

  loadVehicles(): void {
    if (!this.user?.id) {
      this.errorMessage = 'Usuario no autenticado';
      return;
    }

    this.loading = true;
    this.errorMessage = ''; // Limpiamos errores previos al recargar

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

  refresh(): void {
    this.loadVehicles();
  }

  goToCheckIn(vehicle: any): void {
    this.router.navigate(['/parking-entry/entry'], {
      queryParams: {
        vehicle_id: vehicle.id
      }
    });
  }
}