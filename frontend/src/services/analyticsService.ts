import { api } from './api';
import type { APIResponse } from '../types';

export const analyticsService = {
  getResumeAnalytics: async (resumeId: number, days: number = 30): Promise<APIResponse<any>> => {
    return api.get(`/api/analytics/resume/${resumeId}?days=${days}`);
  },

  getDashboardAnalytics: async (days: number = 30): Promise<APIResponse<any>> => {
    return api.get(`/api/analytics/dashboard?days=${days}`);
  }
};
