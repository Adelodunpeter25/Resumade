import { api } from './api';

export interface BulletPointRequest {
  position: string;
  company: string;
  current_description?: string;
  seniority_level?: 'entry' | 'mid' | 'senior';
  industry?: string;
}

export interface ImproveDescriptionRequest {
  current_text: string;
  position: string;
  company: string;
  seniority_level?: 'entry' | 'mid' | 'senior';
}

export interface GenerateSummaryRequest {
  position: string;
  years_experience: number;
  skills: string[];
  industry?: string;
}

export interface AIResponse<T> {
  success: boolean;
  message: string;
  data: T;
}

export const aiService = {
  async generateBulletPoints(data: BulletPointRequest): Promise<AIResponse<{ suggestions: string[]; count: number }>> {
    return api.post('/api/ai/generate-bullets', data);
  },

  async improveDescription(data: ImproveDescriptionRequest): Promise<AIResponse<{ improved_text: string; original_text: string }>> {
    return api.post('/api/ai/improve-description', data);
  },

  async generateSummary(data: GenerateSummaryRequest): Promise<AIResponse<{ summary: string }>> {
    return api.post('/api/ai/generate-summary', data);
  },

  async checkStatus(): Promise<{ available: boolean; model: string | null }> {
    return api.get('/api/ai/status');
  }
};
