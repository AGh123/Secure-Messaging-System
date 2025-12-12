import { Injectable, signal } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class SessionService {
  private readonly TOKEN_KEY = 'ciphercapsule_token';

  readonly token = signal<string | null>(localStorage.getItem(this.TOKEN_KEY));

  readonly user = signal<{ username: string } | null>(null);

  setToken(token: string) {
    localStorage.setItem(this.TOKEN_KEY, token);
    this.token.set(token);
  }

  clear() {
    localStorage.removeItem(this.TOKEN_KEY);
    this.token.set(null);
    this.user.set(null);
  }

  setUser(username: string) {
    this.user.set({ username });
  }

  isLoggedIn(): boolean {
    return !!this.token() && !!this.user();
  }
}
