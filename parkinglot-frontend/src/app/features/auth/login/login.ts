import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './login.html',
  styleUrls: ['./login.css']
})
export class Login {

  loginForm: FormGroup;
  message: string = '';

  constructor(
    private fb: FormBuilder,
    private http: HttpClient,
    private router: Router
  ) {
    this.loginForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(4)]]
    });
  }

  onSubmit(): void {
    if (this.loginForm.invalid) {
      this.loginForm.markAllAsTouched();
      return;
    }

    const data = this.loginForm.value;

    console.log('LOGIN DATA:', data);

    this.http.post('http://localhost:8000/api/auth/login', data)
      .subscribe({
        next: (res: any) => {
          console.log('LOGIN OK:', res);
          this.message = res.message;
          this.router.navigate(['/parking-entry']);
        },
        error: (err) => {
          console.error('LOGIN ERROR:', err);
          this.message = err.error?.detail || 'Error en login';
        }
      });
  }
}