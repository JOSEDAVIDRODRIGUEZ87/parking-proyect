import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({ providedIn: 'root' })
export class AuthService {

    private api = 'http://localhost:8000/api';

    constructor(private http: HttpClient) { }

    login(data: any) {
        return this.http.post(`${this.api}/auth/login`, data);
    }

    saveSession(res: any) {
        localStorage.setItem('user', JSON.stringify(res.user));
    }

    getUser() {
        const user = localStorage.getItem('user');
        return user ? JSON.parse(user) : null;
    }

    logout() {
        localStorage.removeItem('user');
    }
}