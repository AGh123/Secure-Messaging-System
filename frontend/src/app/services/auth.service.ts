import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import {
  RegisterRequest,
  LoginRequest,
  LoginResponse,
  BasicResponse,
} from '../models/auth.model';
import { SessionService } from './session.service';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private http = inject(HttpClient);
  private session = inject(SessionService);

  private readonly baseUrl = 'http://127.0.0.1:8000/auth';

  register(payload: RegisterRequest) {
    return this.http.post<BasicResponse>(`${this.baseUrl}/register`, payload);
  }

  login(payload: LoginRequest) {
    return this.http.post<LoginResponse>(`${this.baseUrl}/login`, payload);
  }

  logout() {
    const token = this.session.token();
    if (!token) return;

    return this.http.post<BasicResponse>(
      `${this.baseUrl}/logout`,
      {},
      {
        headers: new HttpHeaders({
          Authorization: token,
        }),
      }
    );
  }

  /**
   * Verify session on app startup / refresh
   */
  me() {
    const token = this.session.token();
    if (!token) return;

    return this.http.get<{ username: string }>(`${this.baseUrl}/me`, {
      headers: new HttpHeaders({
        Authorization: token,
      }),
    });
  }

  getUsers() {
    const token = this.session.token();
    return this.http.get<string[]>(`${this.baseUrl}/users`, {
      headers: new HttpHeaders({
        Authorization: token ?? '',
      }),
    });
  }
}
