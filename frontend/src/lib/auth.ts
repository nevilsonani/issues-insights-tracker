import { writable } from 'svelte/store';
import { browser } from '$app/environment';
import type { User } from './types';

export const user = writable<User | null>(null);

export function setUser(userData: User) {
  user.set(userData);
}

export function setToken(token: string) {
  if (browser) {
    localStorage.setItem('token', token);
  }
}

export function getToken(): string | null {
  if (browser) {
    return localStorage.getItem('token');
  }
  return null;
}

export function logout() {
  user.set(null);
  if (browser) {
    localStorage.removeItem('token');
  }
}

export function isAuthenticated(): boolean {
  if (browser) {
    return !!getToken();
  }
  return false;
}

// Initialize user from token on app start
export function initializeAuth() {
  if (browser) {
    const token = getToken();
    if (token) {
      // You could decode the JWT token here to get user info
      // For now, we'll rely on the backend to validate the token
    }
  }
}
