import { useEffect, useRef, useCallback } from 'react';
import { API_BASE_URL } from '../services/api';
import type { Resume } from '../types';

export const usePreview = (resume: Partial<Resume>) => {
  const previewIframeRef = useRef<HTMLIFrameElement>(null);
  const timeoutRef = useRef<ReturnType<typeof setTimeout>>();

  const updatePreview = useCallback(() => {
    if (previewIframeRef.current) {
      const iframe = previewIframeRef.current;
      const previewUrl = `${API_BASE_URL}/api/resumes/preview`;
      
      const form = document.createElement('form');
      form.method = 'POST';
      form.action = previewUrl;
      form.target = iframe.name || 'preview-frame';
      form.style.display = 'none';
      
      const input = document.createElement('input');
      input.type = 'hidden';
      input.name = 'resume_data';
      input.value = JSON.stringify(resume);
      
      form.appendChild(input);
      document.body.appendChild(form);
      form.submit();
      document.body.removeChild(form);
    }
  }, [resume]);

  useEffect(() => {
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }
    
    timeoutRef.current = setTimeout(() => {
      updatePreview();
    }, 300);

    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, [updatePreview]);

  return { previewIframeRef };
};
