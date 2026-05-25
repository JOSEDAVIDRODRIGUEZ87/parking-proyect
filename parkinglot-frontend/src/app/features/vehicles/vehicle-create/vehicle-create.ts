import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { AuthService } from '../../../core/services/auth.service';

@Component({
  selector: 'app-vehicle-create',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './vehicle-create.html',
  styleUrls: ['./vehicle-create.css']
})
export class VehicleCreate {

  form: FormGroup;
  user: any = null;

  loading = false;
  successMessage = '';
  errorMessage = '';

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private http: HttpClient
  ) {

    // 👤 usuario desde sesión
    this.user = this.authService.getUser();

    console.log('USER VEHICLE CREATE:', this.user);

    this.form = this.fb.group({
      plate: ['', [Validators.required, Validators.minLength(5)]],
      brand: ['', [Validators.required]],
      model: ['', [Validators.required]],
      color: ['', [Validators.required]],
      vehicle_type: ['', [Validators.required]]
    });
  }

  onSubmit() {

    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    if (!this.user?.id) {
      this.errorMessage = 'Usuario no autenticado';
      return;
    }

    this.loading = true;
    this.successMessage = '';
    this.errorMessage = '';

    const payload = {
      plate: this.form.value.plate,
      brand: this.form.value.brand,
      model: this.form.value.model,
      color: this.form.value.color,
      vehicle_type: this.form.value.vehicle_type, // CAR | MOTORCYCLE | BICYCLE
      user_id: this.user.id
    };

    console.log('VEHICLE PAYLOAD:', payload);

    this.http.post('http://localhost:8000/api/vehicles', payload)
      .subscribe({
        next: (res: any) => {

          this.successMessage = 'Vehículo registrado correctamente 🚗';
          this.errorMessage = '';

          this.form.reset();
          this.loading = false;
        },

        error: (err) => {

          console.error(err);

          this.errorMessage = err.error?.detail || 'Error registrando vehículo';
          this.loading = false;
        }
      });
  }
}