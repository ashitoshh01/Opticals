'use client';
import { create } from 'zustand';
import { User } from '@/lib/types';
import { authApi } from '@/lib/api';

interface AuthState {
  user: User | null;
  token: string | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  signup: (name: string, email: string, password: string) => Promise<void>;
  logout: () => void;
  loadUser: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  token: typeof window !== 'undefined' ? localStorage.getItem('token') : null,
  loading: true,

  login: async (email, password) => {
    const res = await authApi.login({ email, password });
    localStorage.setItem('token', res.access_token);
    set({ user: res.user, token: res.access_token });
  },

  signup: async (name, email, password) => {
    const res = await authApi.signup({ name, email, password });
    localStorage.setItem('token', res.access_token);
    set({ user: res.user, token: res.access_token });
  },

  logout: () => {
    localStorage.removeItem('token');
    set({ user: null, token: null });
  },

  loadUser: async () => {
    const token = localStorage.getItem('token');
    if (!token) {
      set({ loading: false });
      return;
    }
    try {
      const user = await authApi.me();
      set({ user, token, loading: false });
    } catch {
      localStorage.removeItem('token');
      set({ user: null, token: null, loading: false });
    }
  },
}));
