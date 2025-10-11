import { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { resumeService } from '../services';
import type { Resume, Template } from '../types';
import { useErrorHandler } from './useErrorHandler';
import { useSaveManager } from './useSaveManager';

const GUEST_RESUME_KEY = 'guest_resume';

export const useResumeBuilder = (id?: string) => {
  const navigate = useNavigate();
  const { showError, showWarning } = useErrorHandler();
  const { saving, saveStatus, executeSave, debouncedSave, markUnsaved } = useSaveManager();
  
  const [resume, setResume] = useState<Partial<Resume>>({
    title: 'Untitled Resume',
    template_name: 'professional-blue',
    personal_info: {
      full_name: '', email: '', phone: '', location: '',
      linkedin: '', website: '', summary: ''
    },
    experience: [], education: [], skills: [],
    certifications: [], projects: []
  });
  
  const [templates, setTemplates] = useState<{ categories: Record<string, Template[]>, all_templates: Template[] }>({
    categories: {},
    all_templates: []
  });
  const [loading, setLoading] = useState(!!id);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('token');
    setIsAuthenticated(!!token);
    
    loadTemplates();
    
    if (id && id !== 'new') {
      if (token) {
        loadResume();
      } else {
        navigate('/login');
      }
    } else if (id === 'new' && !token) {
      const savedResume = localStorage.getItem(GUEST_RESUME_KEY);
      if (savedResume) {
        setResume(JSON.parse(savedResume));
      }
      setLoading(false);
    } else {
      setLoading(false);
    }
  }, [id]);

  const loadTemplates = async () => {
    try {
      const response = await resumeService.getTemplates();
      if (response.success && response.data) {
        setTemplates(response.data);
      }
    } catch (err) {
      showWarning('Failed to load templates, using defaults');
      setTemplates({
        categories: {
          professional: [
            { name: 'professional-blue', display_name: 'Professional Blue', description: 'Clean and professional', category: 'professional', industry: ['business'], ats_score: 90 }
          ]
        },
        all_templates: [
          { name: 'professional-blue', display_name: 'Professional Blue', description: 'Clean and professional', category: 'professional', industry: ['business'], ats_score: 90 }
        ]
      });
    }
  };

  const loadResume = async () => {
    try {
      const response = await resumeService.getResume(Number(id));
      if (response.success && response.data) {
        setResume(response.data);
      }
    } catch (err) {
      showError(err, 'Failed to load resume');
      navigate('/dashboard');
    } finally {
      setLoading(false);
    }
  };

  const performSave = async () => {
    if (!isAuthenticated) {
      localStorage.setItem(GUEST_RESUME_KEY, JSON.stringify(resume));
    } else if (id && id !== 'new') {
      await resumeService.updateResume(Number(id), resume);
    } else {
      const response = await resumeService.createResume(resume);
      if (response.success && response.data) {
        navigate(`/resume/${response.data.id}`, { replace: true });
      }
    }
  };

  const handleSave = async (isAutosave = false) => {
    try {
      await executeSave(performSave, isAutosave);
    } catch (err) {
      showError(err, 'Failed to save resume');
    }
  };

  const updateResumeData = useCallback((field: string, value: any) => {
    setResume(prev => ({ ...prev, [field]: value }));
    markUnsaved();
    debouncedSave(performSave);
  }, [markUnsaved, debouncedSave]);

  return {
    resume, templates, saving, saveStatus, loading, isAuthenticated,
    handleSave, updateResumeData, setResume
  };
};
