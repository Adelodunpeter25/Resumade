import { useState, useRef, useCallback } from 'react';

export const useSaveManager = () => {
  const [saving, setSaving] = useState(false);
  const [saveStatus, setSaveStatus] = useState<'saved' | 'saving' | 'unsaved'>('saved');
  const saveOperationRef = useRef<Promise<void> | null>(null);
  const debounceTimeoutRef = useRef<NodeJS.Timeout | null>(null);

  const executeSave = useCallback(async (saveFunction: () => Promise<void>, isAutosave = false) => {
    // Prevent multiple simultaneous saves
    if (saveOperationRef.current) {
      await saveOperationRef.current;
    }

    if (!isAutosave) setSaving(true);
    setSaveStatus('saving');

    const savePromise = (async () => {
      try {
        await saveFunction();
        setSaveStatus('saved');
      } catch (error) {
        setSaveStatus('unsaved');
        throw error;
      } finally {
        if (!isAutosave) setSaving(false);
        saveOperationRef.current = null;
      }
    })();

    saveOperationRef.current = savePromise;
    return savePromise;
  }, []);

  const debouncedSave = useCallback((saveFunction: () => Promise<void>, delay = 1000) => {
    if (debounceTimeoutRef.current) {
      clearTimeout(debounceTimeoutRef.current);
    }

    debounceTimeoutRef.current = setTimeout(() => {
      executeSave(saveFunction, true);
    }, delay);
  }, [executeSave]);

  const markUnsaved = useCallback(() => {
    setSaveStatus('unsaved');
  }, []);

  return {
    saving,
    saveStatus,
    executeSave,
    debouncedSave,
    markUnsaved
  };
};
