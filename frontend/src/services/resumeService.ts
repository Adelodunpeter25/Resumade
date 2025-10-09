import { api, API_BASE_URL } from './api';
import type { Resume, APIResponse, ShareLink, ResumeVersion, Template } from '../types';

export const resumeService = {
  getResumes: async (page = 1, size = 20): Promise<APIResponse<{ items: Resume[]; total: number; page: number; size: number }>> => {
    return api.get(`/api/resumes/?page=${page}&size=${size}`);
  },

  getResume: async (id: number): Promise<APIResponse<Resume>> => {
    return api.get(`/api/resumes/${id}`);
  },

  createResume: async (data: Partial<Resume>): Promise<APIResponse<Resume>> => {
    return api.post('/api/resumes/', data);
  },

  updateResume: async (id: number, data: Partial<Resume>): Promise<APIResponse<Resume>> => {
    return api.put(`/api/resumes/${id}`, data);
  },

  deleteResume: async (id: number): Promise<APIResponse<null>> => {
    return api.delete(`/api/resumes/${id}`);
  },

  getVersions: async (id: number): Promise<APIResponse<ResumeVersion[]>> => {
    return api.get(`/api/resumes/${id}/versions`);
  },

  createVersion: async (id: number): Promise<APIResponse<ResumeVersion>> => {
    return api.post(`/api/resumes/${id}/versions`, {});
  },

  createShareLink: async (id: number, expires_in_days: number): Promise<APIResponse<ShareLink>> => {
    return api.post(`/api/resumes/${id}/share`, { expires_in_days });
  },

  getShareLinks: async (id: number): Promise<APIResponse<ShareLink[]>> => {
    return api.get(`/api/resumes/${id}/share`);
  },

  deleteShareLink: async (resumeId: number, token: string): Promise<APIResponse<null>> => {
    return api.delete(`/api/resumes/${resumeId}/share/${token}`);
  },

  getSharedResume: async (token: string): Promise<APIResponse<Resume>> => {
    return api.get(`/api/resumes/shared/${token}`);
  },

  getTemplates: async (): Promise<APIResponse<Template[]>> => {
    return api.get('/api/resumes/templates');
  },

  previewTemplate: async (templateName: string, resumeId?: number): Promise<Blob> => {
    const endpoint = resumeId 
      ? `/api/resumes/templates/preview?template=${templateName}&resume_id=${resumeId}`
      : `/api/resumes/templates/preview?template=${templateName}`;
    
    const token = localStorage.getItem('token');
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      headers: token ? { 'Authorization': `Bearer ${token}` } : {}
    });
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    return response.blob();
  },

  downloadPDF: async (id: number, template?: string): Promise<Blob> => {
    const endpoint = template 
      ? `/api/resumes/${id}/pdf?template=${template}`
      : `/api/resumes/${id}/pdf`;
    
    const token = localStorage.getItem('token');
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      headers: token ? { 'Authorization': `Bearer ${token}` } : {}
    });
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    return response.blob();
  },

  generateGuestPDF: async (resumeData: any, template: string = 'professional-blue'): Promise<Blob> => {
    const response = await fetch(`${API_BASE_URL}/api/resumes/generate-pdf?template=${template}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(resumeData)
    });
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    return response.blob();
  }
};
