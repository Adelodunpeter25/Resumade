import { api } from './api';

export interface ATSScore {
  resume_id: number;
  ats_score: number;
  grade: string;
  feedback: string[];
  ai_feedback?: string;
  ai_suggestions?: string[];
  section_breakdown: {
    [key: string]: {
      score: number;
      max_score: number;
      percentage: number;
    };
  };
  formatting_check: {
    [key: string]: boolean;
  };
  suggestions: string[];
  role_level: string;
  job_matched: boolean;
}

export const atsService = {
  calculateScore: async (resumeId: number): Promise<ATSScore> => {
    return api.get(`/api/resumes/${resumeId}/score`);
  }
};
