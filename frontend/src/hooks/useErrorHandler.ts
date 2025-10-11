import { useState, useCallback } from 'react';

interface ErrorState {
  message: string;
  type: 'error' | 'warning' | 'info';
  visible: boolean;
}

export const useErrorHandler = () => {
  const [error, setError] = useState<ErrorState>({ message: '', type: 'error', visible: false });

  const showError = useCallback((err: any, context?: string) => {
    let message = 'An unexpected error occurred';
    
    if (err?.response?.data?.message) {
      message = err.response.data.message;
    } else if (err?.message) {
      message = err.message;
    } else if (typeof err === 'string') {
      message = err;
    }

    if (context) {
      message = `${context}: ${message}`;
    }

    setError({ message, type: 'error', visible: true });
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
      setError(prev => ({ ...prev, visible: false }));
    }, 5000);
  }, []);

  const showWarning = useCallback((message: string) => {
    setError({ message, type: 'warning', visible: true });
    setTimeout(() => {
      setError(prev => ({ ...prev, visible: false }));
    }, 4000);
  }, []);

  const hideError = useCallback(() => {
    setError(prev => ({ ...prev, visible: false }));
  }, []);

  return { error, showError, showWarning, hideError };
};
