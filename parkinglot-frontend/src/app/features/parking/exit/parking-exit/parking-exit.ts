import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-parking-exit',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './parking-exit.html',
  styleUrls: ['./parking-exit.css']
})
export class ParkingExit {

  parkingEntryId: string | null = null;

  entry: any = null;

  loading = false;
  successMessage = '';
  errorMessage = '';

  constructor(
    private http: HttpClient,
    private route: ActivatedRoute,
    private router: Router
  ) {

    this.route.queryParams.subscribe(params => {

      this.parkingEntryId = params['parking_entry_id'];

      if (this.parkingEntryId) {
        this.loadEntry(this.parkingEntryId);
      }
    });
  }

  loadEntry(id: string) {

    this.http.get(`http://localhost:8000/api/parking-entries/${id}`)
      .subscribe({
        next: (res) => {
          this.entry = res;
        },
        error: (err) => {
          console.error(err);
          this.errorMessage = 'No se pudo cargar el registro';
        }
      });
  }

  checkOut() {

    if (!this.parkingEntryId) return;

    this.loading = true;
    this.errorMessage = '';
    this.successMessage = '';

    this.http.put(
      `http://localhost:8000/api/parking-entries/check-out/${this.parkingEntryId}`,
      {}
    ).subscribe({
      next: (res: any) => {

        this.successMessage = 'Salida registrada correctamente 🚪';

        this.loading = false;

        // opcional: volver a lista
        setTimeout(() => {
          this.router.navigate(['/vehicle-list']);
        }, 1200);
      },
      error: (err) => {

        console.error(err);

        this.errorMessage = err.error?.detail || 'Error en check-out';

        this.loading = false;
      }
    });
  }
}