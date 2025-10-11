import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { resumeService } from '../services';
import type { Resume } from '../types';
import { useErrorHandler } from './useErrorHandler';

export const useResumeActions = (
  resume: Partial<Resume>, 
  isAuthenticated: boolean, 
  id?: string
) => {
  const navigate = useNavigate();
  const { showError } = useErrorHandler();
  const [downloading, setDownloading] = useState(false);

  const handleDownload = async (format: 'pdf' | 'docx' | 'txt' = 'pdf') => {
    setDownloading(true);
    try {
      let blob: Blob;
      let filename: string;
      
      if (isAuthenticated && id && id !== 'new') {
        const response = await resumeService.exportResume(Number(id), format);
        blob = new Blob([response], { 
          type: format === 'pdf' ? 'application/pdf' : 
                format === 'docx' ? 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' :
                'text/plain'
        });
        filename = `${resume.title || 'resume'}.${format}`;
      } else {
        const response = await resumeService.generateGuestPDF(resume, resume.template_name || 'professional-blue');
        blob = new Blob([response], { type: 'application/pdf' });
        filename = `${resume.title || 'resume'}.pdf`;
      }
      
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (err) {
      showError(err, 'Failed to download resume');
    } finally {
      setDownloading(false);
    }
  };

  const handleFeatureClick = (feature: string) => {
    if (!isAuthenticated) {
      if (confirm(`${feature} requires an account. Would you like to login or sign up?`)) {
        navigate('/login');
      }
      return;
    }
    
    switch(feature) {
      case 'versions':
        navigate(`/resume/${id}/versions`);
        break;
      case 'ats':
        navigate(`/resume/${id}/ats-score`);
        break;
      case 'preview':
        navigate(`/resume/${id}/preview`);
        break;
    }
  };

  return { downloading, handleDownload, handleFeatureClick };
};
