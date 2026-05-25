import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { AuthService } from '../../../core/services/auth.service';

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
  loading = false;

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
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

    this.loading = true;

    const data = this.loginForm.value;

    this.authService.login(data).subscribe({
      next: (res: any) => {

        console.log('LOGIN OK:', res);

        // 🔐 guardar token + user
        this.authService.saveSession(res);

        this.message = 'Login exitoso';

        // 🚗 redirección correcta
        this.router.navigate(['/vehicles/list']);

        this.loading = false;
      },

      error: (err) => {
        console.error('LOGIN ERROR:', err);

        this.message = err.error?.detail || 'Error en login';

        this.loading = false;
      }
    });
  }
}