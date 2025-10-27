import { useState } from 'react';
import { Sparkles, Loader2, Check, X, RefreshCw } from 'lucide-react';
import { aiService } from '../../services';

interface Props {
  position: string;
  company: string;
  currentDescription?: string;
  seniorityLevel?: 'entry' | 'mid' | 'senior';
  onInsert: (text: string) => void;
  onClose: () => void;
}

export default function AIBulletSuggester({
  position,
  company,
  currentDescription,
  seniorityLevel = 'mid',
  onInsert,
  onClose
}: Props) {
  const [loading, setLoading] = useState(false);
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [error, setError] = useState('');
  const [selectedBullets, setSelectedBullets] = useState<Set<number>>(new Set());

  const generateSuggestions = async () => {
    if (!position || !company) {
      setError('Please fill in position and company first');
      return;
    }

    setLoading(true);
    setError('');
    setSuggestions([]);
    setSelectedBullets(new Set());

    try {
      const response = await aiService.generateBulletPoints({
        position,
        company,
        current_description: currentDescription,
        seniority_level: seniorityLevel
      });

      if (response.success && response.data.suggestions) {
        setSuggestions(response.data.suggestions);
      } else {
        setError('Failed to generate suggestions');
      }
    } catch (err: any) {
      setError(err.message || 'Failed to generate suggestions. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const toggleBullet = (index: number) => {
    const newSelected = new Set(selectedBullets);
    if (newSelected.has(index)) {
      newSelected.delete(index);
    } else {
      newSelected.add(index);
    }
    setSelectedBullets(newSelected);
  };

  const insertSelected = () => {
    const selectedText = suggestions
      .filter((_, index) => selectedBullets.has(index))
      .map(bullet => `• ${bullet}`)
      .join('\n');
    
    if (selectedText) {
      onInsert(selectedText);
      onClose();
    }
  };

  const insertAll = () => {
    const allText = suggestions
      .map(bullet => `• ${bullet}`)
      .join('\n');
    
    if (allText) {
      onInsert(allText);
      onClose();
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-3xl w-full max-h-[90vh] overflow-hidden flex flex-col">
        {/* Header */}
        <div className="px-6 py-4 border-b border-gray-200 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Sparkles className="text-purple-600" size={24} />
            <h3 className="text-xl font-bold text-gray-900">AI Bullet Point Generator</h3>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600"
          >
            <X size={24} />
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-6">
          {/* Context Info */}
          <div className="bg-purple-50 rounded-lg p-4 mb-6">
            <div className="text-sm text-gray-700">
              <p><strong>Position:</strong> {position}</p>
              <p><strong>Company:</strong> {company}</p>
              <p><strong>Level:</strong> {seniorityLevel}</p>
            </div>
          </div>

          {/* Generate Button */}
          {suggestions.length === 0 && !loading && (
            <div className="text-center py-8">
              <button
                onClick={generateSuggestions}
                disabled={loading || !position || !company}
                className="inline-flex items-center gap-2 bg-gradient-to-r from-purple-600 to-indigo-600 text-white px-6 py-3 rounded-lg hover:from-purple-700 hover:to-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed font-medium"
              >
                <Sparkles size={20} />
                Generate AI Suggestions
              </button>
              <p className="text-sm text-gray-500 mt-3">
                Get 5 professional bullet points tailored to your role
              </p>
            </div>
          )}

          {/* Loading State */}
          {loading && (
            <div className="text-center py-12">
              <Loader2 className="animate-spin text-purple-600 mx-auto mb-4" size={48} />
              <p className="text-gray-600">Generating suggestions...</p>
              <p className="text-sm text-gray-500 mt-2">This may take a few seconds</p>
            </div>
          )}

          {/* Error State */}
          {error && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-4">
              <p className="text-red-800">{error}</p>
            </div>
          )}

          {/* Suggestions */}
          {suggestions.length > 0 && !loading && (
            <div className="space-y-3">
              <div className="flex items-center justify-between mb-4">
                <p className="text-sm text-gray-600">
                  Select the bullet points you want to use:
                </p>
                <button
                  onClick={generateSuggestions}
                  className="flex items-center gap-1 text-sm text-purple-600 hover:text-purple-700"
                >
                  <RefreshCw size={16} />
                  Regenerate
                </button>
              </div>

              {suggestions.map((suggestion, index) => (
                <div
                  key={index}
                  onClick={() => toggleBullet(index)}
                  className={`p-4 rounded-lg border-2 cursor-pointer transition-all ${
                    selectedBullets.has(index)
                      ? 'border-purple-500 bg-purple-50'
                      : 'border-gray-200 hover:border-purple-300 bg-white'
                  }`}
                >
                  <div className="flex items-start gap-3">
                    <div className={`flex-shrink-0 w-5 h-5 rounded border-2 flex items-center justify-center mt-0.5 ${
                      selectedBullets.has(index)
                        ? 'border-purple-500 bg-purple-500'
                        : 'border-gray-300'
                    }`}>
                      {selectedBullets.has(index) && (
                        <Check size={14} className="text-white" />
                      )}
                    </div>
                    <p className="text-gray-800 flex-1">• {suggestion}</p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Footer */}
        {suggestions.length > 0 && !loading && (
          <div className="px-6 py-4 border-t border-gray-200 flex items-center justify-between bg-gray-50">
            <p className="text-sm text-gray-600">
              {selectedBullets.size} of {suggestions.length} selected
            </p>
            <div className="flex gap-3">
              <button
                onClick={onClose}
                className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-100"
              >
                Cancel
              </button>
              <button
                onClick={insertAll}
                className="px-4 py-2 border border-purple-300 text-purple-600 rounded-lg hover:bg-purple-50"
              >
                Insert All
              </button>
              <button
                onClick={insertSelected}
                disabled={selectedBullets.size === 0}
                className="px-4 py-2 bg-gradient-to-r from-purple-600 to-indigo-600 text-white rounded-lg hover:from-purple-700 hover:to-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Insert Selected ({selectedBullets.size})
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
