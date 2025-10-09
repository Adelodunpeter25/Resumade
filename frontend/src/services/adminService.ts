import { api } from './api';
import type { User, Resume, APIResponse } from '../types';

export interface DashboardStats {
  total_users: number;
  active_users: number;
  new_users_this_week: number;
  total_resumes: number;
  total_views: number;
  total_downloads: number;
  average_ats_score: number;
  template_usage: Record<string, number>;
  active_share_links: number;
}

export const adminService = {
  getDashboard: async (): Promise<APIResponse<DashboardStats>> => {
    return api.get('/api/admin/dashboard');
  },

  getUsers: async (page = 1, size = 20): Promise<APIResponse<{ items: User[]; total: number; page: number; size: number }>> => {
    return api.get(`/api/admin/users?page=${page}&size=${size}`);
  },

  getResumes: async (page = 1, size = 20): Promise<APIResponse<{ items: Resume[]; total: number; page: number; size: number }>> => {
    return api.get(`/api/admin/resumes?page=${page}&size=${size}`);
  }
};
