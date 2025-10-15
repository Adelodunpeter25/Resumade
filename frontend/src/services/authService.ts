import { api } from './api';
import type { User, APIResponse } from '../types';

export const authService = {
  register: async (email: string, password: string, full_name: string): Promise<APIResponse<{ access_token: string; token_type: string }>> => {
    return api.post('/api/auth/signup', { email, password, full_name });
  },

  login: async (email: string, password: string): Promise<APIResponse<{ access_token: string; user: User }>> => {
    return api.post('/api/auth/login', { email, password });
  },

  logout: async (): Promise<APIResponse<null>> => {
    return api.post('/api/auth/logout', {});
  },

  getCurrentUser: async (): Promise<APIResponse<User>> => {
    return api.get('/api/auth/me');
  },

  forgotPassword: async (email: string): Promise<APIResponse<null>> => {
    return api.post('/api/auth/forgot-password', { email });
  },

  resetPassword: async (token: string, new_password: string): Promise<APIResponse<null>> => {
    return api.post('/api/auth/reset-password', { token, new_password });
  }
};
