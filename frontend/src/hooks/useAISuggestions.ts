import { useState } from 'react';
import { aiService } from '../services';

export function useAISuggestions() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const generateBullets = async (
    position: string,
    company: string,
    currentDescription?: string,
    seniorityLevel: 'entry' | 'mid' | 'senior' = 'mid'
  ) => {
    setLoading(true);
    setError(null);

    try {
      const response = await aiService.generateBulletPoints({
        position,
        company,
        current_description: currentDescription,
        seniority_level: seniorityLevel
      });

      if (response.success) {
        return response.data.suggestions;
      } else {
        throw new Error('Failed to generate suggestions');
      }
    } catch (err: any) {
      const errorMsg = err.message || 'Failed to generate suggestions';
      setError(errorMsg);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const improveDescription = async (
    currentText: string,
    position: string,
    company: string,
    seniorityLevel: 'entry' | 'mid' | 'senior' = 'mid'
  ) => {
    setLoading(true);
    setError(null);

    try {
      const response = await aiService.improveDescription({
        current_text: currentText,
        position,
        company,
        seniority_level: seniorityLevel
      });

      if (response.success) {
        return response.data.improved_text;
      } else {
        throw new Error('Failed to improve description');
      }
    } catch (err: any) {
      const errorMsg = err.message || 'Failed to improve description';
      setError(errorMsg);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const generateSummary = async (
    position: string,
    yearsExperience: number,
    skills: string[],
    industry?: string
  ) => {
    setLoading(true);
    setError(null);

    try {
      const response = await aiService.generateSummary({
        position,
        years_experience: yearsExperience,
        skills,
        industry
      });

      if (response.success) {
        return response.data.summary;
      } else {
        throw new Error('Failed to generate summary');
      }
    } catch (err: any) {
      const errorMsg = err.message || 'Failed to generate summary';
      setError(errorMsg);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return {
    loading,
    error,
    generateBullets,
    improveDescription,
    generateSummary
  };
}
