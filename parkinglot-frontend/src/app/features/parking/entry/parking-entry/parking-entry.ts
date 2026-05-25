import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { AuthService } from '../../../../core/services/auth.service';

@Component({
  selector: 'app-parking-entry',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './parking-entry.html',
  styleUrls: ['./parking-entry.css']
})
export class ParkingEntry {

  form: FormGroup;
  now = new Date();

  user: any = null;

  loading = false;
  successMessage = '';
  errorMessage = '';

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private http: HttpClient
  ) {

    // 🔐 usuario seguro desde localStorage
    this.user = this.authService.getUser() || {};

    console.log('USER COMPLETO:', this.user);

    this.form = this.fb.group({
      plate: ['', [Validators.required, Validators.minLength(5)]],
      vehicleType: ['', Validators.required],
      notes: ['']
    });
  }

  onSubmit() {

    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    if (!this.user || !this.user.id) {
      this.errorMessage = 'Usuario no autenticado';
      return;
    }

    this.loading = true;
    this.successMessage = '';
    this.errorMessage = '';

    const payload = {
      user_id: this.user.id,
      plate: this.form.value.plate,
      vehicle_type: this.form.value.vehicleType,
      notes: this.form.value.notes,
      entry_time: new Date()
    };

    console.log('CHECK-IN PAYLOAD:', payload);

    this.http.post('http://localhost:8000/api/parking-entry', payload)
      .subscribe({
        next: (res: any) => {

          this.successMessage = 'Ingreso registrado correctamente 🚗';
          this.loading = false;

          this.form.reset();
        },

        error: (err) => {

          console.error(err);

          this.errorMessage =
            err.error?.detail || 'Error registrando ingreso';

          this.loading = false;
        }
      });
  }
}