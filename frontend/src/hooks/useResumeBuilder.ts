import { useState, useEffect, useCallback } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { resumeService } from '../services';
import type { Resume, Template } from '../types';
import { useErrorHandler } from './useErrorHandler';
import { useSaveManager } from './useSaveManager';

const GUEST_RESUME_KEY = 'guest_resume';
const MAX_STORAGE_SIZE = 20 * 1024 * 1024; // 20MB

const getStorageSize = (data: string): number => {
  return new Blob([data]).size;
};

const canStoreData = (data: string): boolean => {
  const size = getStorageSize(data);
  return size <= MAX_STORAGE_SIZE;
};

export const useResumeBuilder = (id?: string) => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const { showError, showWarning } = useErrorHandler();
  const { saving, saveStatus, executeSave, debouncedSave, markUnsaved } = useSaveManager();
  
  // Get template from URL parameter
  const templateParam = searchParams.get('template');
  
  const [resume, setResume] = useState<Partial<Resume>>({
    title: 'Untitled Resume',
    template_name: templateParam || 'professional-blue',
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
    
    // Update template if parameter changes
    if (templateParam && templateParam !== resume.template_name) {
      setResume(prev => ({ ...prev, template_name: templateParam }));
    }
    
    if (id && id !== 'new') {
      if (token) {
        loadResume();
      } else {
        navigate('/login');
      }
    } else if (id === 'new' && !token) {
      const savedResume = localStorage.getItem(GUEST_RESUME_KEY);
      if (savedResume) {
        const parsed = JSON.parse(savedResume);
        // Override template if parameter is provided
        if (templateParam) {
          parsed.template_name = templateParam;
        }
        setResume(parsed);
      }
      setLoading(false);
    } else {
      setLoading(false);
    }
  }, [id, templateParam]);

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
      const data = JSON.stringify(resume);
      if (!canStoreData(data)) {
        const sizeMB = (getStorageSize(data) / (1024 * 1024)).toFixed(2);
        showError(
          new Error(`Resume data (${sizeMB}MB) exceeds 20MB limit. Please login to save larger resumes.`),
          'Storage Limit Exceeded'
        );
        return;
      }
      localStorage.setItem(GUEST_RESUME_KEY, data);
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
