import { api } from './api';
import type { APIResponse } from '../types';

export interface ATSScore {
  overall_score: number;
  section_scores: {
    personal_info: number;
    experience: number;
    education: number;
    skills: number;
    certifications: number;
    projects: number;
  };
  suggestions: string[];
  missing_sections: string[];
}

export const atsService = {
  calculateScore: async (resumeId: number): Promise<APIResponse<ATSScore>> => {
    return api.post(`/api/ats/calculate/${resumeId}`, {});
  }
};
