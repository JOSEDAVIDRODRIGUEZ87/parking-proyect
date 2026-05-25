import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { AuthService } from '../../../../core/services/auth.service';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-parking-entry',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './parking-entry.html',
  styleUrls: ['./parking-entry.css']
})
export class ParkingEntry {

  form: FormGroup;
  user: any = null;

  vehicleId: string | null = null;

  loading = false;
  successMessage = '';
  errorMessage = '';

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private http: HttpClient,
    private route: ActivatedRoute
  ) {

    this.user = this.authService.getUser();

    this.form = this.fb.group({
      plate: ['', Validators.required],
      vehicle_type: ['', Validators.required],
      notes: ['']
    });

    // 📥 recibir vehicle_id desde navegación
    this.route.queryParams.subscribe(params => {

      this.vehicleId = params['vehicle_id'];

      console.log('VEHICLE ID:', this.vehicleId);

      if (this.vehicleId) {
        this.loadVehicle(this.vehicleId);
      }
    });
  }

  loadVehicle(id: string) {

    this.http.get<any>(`http://localhost:8000/api/vehicles/${id}`)
      .subscribe({
        next: (vehicle) => {

          this.form.patchValue({
            plate: vehicle.plate,
            vehicle_type: vehicle.vehicle_type
          });

        },
        error: (err) => {
          console.error(err);
        }
      });
  }

  onSubmit() {

    if (!this.vehicleId || !this.user?.id) {
      this.errorMessage = 'Datos incompletos';
      return;
    }

    this.loading = true;
    this.errorMessage = '';
    this.successMessage = '';

    const payload = {
      vehicle_id: this.vehicleId,
      notes: this.form.value.notes
    };

    console.log('CHECK-IN PAYLOAD:', payload);

    this.http.post(
      'http://localhost:8000/api/parking-entries/check-in',
      payload
    ).subscribe({
      next: () => {
        this.successMessage = 'Check-in registrado 🚗';
        this.loading = false;
      },
      error: (err) => {
        console.error(err);
        this.errorMessage = err.error?.detail || 'Error registrando check-in';
        this.loading = false;
      }
    });
  }
}