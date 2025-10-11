import { useState } from 'react';
import { Check, Star, Zap } from 'lucide-react';
import { API_BASE_URL } from '../../services/api';
import type { Template } from '../../types';

interface Props {
  templates: { categories: Record<string, Template[]>, all_templates: Template[] };
  currentTemplate: string;
  onTemplateChange: (templateName: string) => void;
  onClose: () => void;
}

const categoryIcons = {
  technology: '💻',
  creative: '🎨',
  executive: '👔',
  marketing: '📈',
  academic: '🎓',
  professional: '💼',
  minimalist: '⚡',
  modern: '🚀',
  traditional: '📋'
};

const categoryDescriptions = {
  technology: 'Perfect for software engineers and tech professionals',
  creative: 'Designed for designers, artists, and creative roles',
  executive: 'Professional layouts for senior management positions',
  marketing: 'Dynamic designs for marketing and sales professionals',
  academic: 'Traditional formats for researchers and educators',
  professional: 'Classic business layouts for corporate roles',
  minimalist: 'Clean, simple designs that focus on content',
  modern: 'Contemporary layouts for forward-thinking professionals',
  traditional: 'Time-tested formats for conservative industries'
};

export default function TemplateSelector({ templates, currentTemplate, onTemplateChange, onClose }: Props) {
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [loadingPreviews, setLoadingPreviews] = useState<Record<string, boolean>>({});

  const categories = Object.keys(templates.categories);
  const displayTemplates = selectedCategory 
    ? templates.categories[selectedCategory] || []
    : templates.all_templates;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-xl shadow-2xl max-w-7xl w-full max-h-[90vh] overflow-hidden">
        <div className="p-6 border-b border-gray-200">
          <div className="flex justify-between items-center">
            <div>
              <h2 className="text-2xl font-bold text-gray-900">Choose Your Template</h2>
              <p className="text-gray-600 mt-1">Select a professional template that matches your industry</p>
            </div>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600 text-2xl"
            >
              ×
            </button>
          </div>
          
          {/* Category Filter */}
          <div className="flex flex-wrap gap-2 mt-4">
            <button
              onClick={() => setSelectedCategory(null)}
              className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
                selectedCategory === null
                  ? 'bg-emerald-100 text-emerald-700 border-2 border-emerald-300'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              All Templates ({templates.all_templates.length})
            </button>
            {categories.map((category) => (
              <button
                key={category}
                onClick={() => setSelectedCategory(category)}
                className={`px-4 py-2 rounded-full text-sm font-medium transition-colors flex items-center gap-2 ${
                  selectedCategory === category
                    ? 'bg-emerald-100 text-emerald-700 border-2 border-emerald-300'
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }`}
              >
                <span>{categoryIcons[category as keyof typeof categoryIcons] || '📄'}</span>
                {category.charAt(0).toUpperCase() + category.slice(1)}
                <span className="text-xs">({templates.categories[category].length})</span>
              </button>
            ))}
          </div>
        </div>
        
        <div className="p-6 overflow-y-auto max-h-[calc(90vh-200px)]">
          {selectedCategory && (
            <div className="mb-6 p-4 bg-gray-50 rounded-lg">
              <h3 className="font-semibold text-gray-900 flex items-center gap-2">
                <span>{categoryIcons[selectedCategory as keyof typeof categoryIcons]}</span>
                {selectedCategory.charAt(0).toUpperCase() + selectedCategory.slice(1)} Templates
              </h3>
              <p className="text-sm text-gray-600 mt-1">
                {categoryDescriptions[selectedCategory as keyof typeof categoryDescriptions]}
              </p>
            </div>
          )}
          
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
            {displayTemplates.map((template) => (
              <div
                key={template.name}
                className={`relative border-2 rounded-lg overflow-hidden cursor-pointer transition-all hover:shadow-md ${
                  currentTemplate === template.name
                    ? 'border-emerald-500 ring-2 ring-emerald-200'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
                onClick={() => onTemplateChange(template.name)}
              >
                {/* Template Preview */}
                <div className="aspect-[3/4] bg-gray-50 relative overflow-hidden">
                  {loadingPreviews[template.name] && (
                    <div className="absolute inset-0 flex items-center justify-center bg-gray-100">
                      <div className="w-4 h-4 border-2 border-emerald-500 border-t-transparent rounded-full animate-spin"></div>
                    </div>
                  )}
                  <iframe
                    src={`${API_BASE_URL}/api/resumes/templates/preview?template=${template.name}`}
                    className="w-full h-full border-0 pointer-events-none"
                    style={{ transform: 'scale(0.6)', transformOrigin: 'top left', width: '167%', height: '167%' }}
                    title={`${template.display_name} Preview`}
                    onLoad={() => setLoadingPreviews(prev => ({ ...prev, [template.name]: false }))}
                    onLoadStart={() => setLoadingPreviews(prev => ({ ...prev, [template.name]: true }))}
                  />
                </div>
                
                {/* Template Info */}
                <div className="p-3">
                  <div className="flex justify-between items-start mb-1">
                    <h3 className="font-semibold text-sm text-gray-900 truncate">{template.display_name}</h3>
                    {currentTemplate === template.name && (
                      <div className="text-emerald-500 ml-1 flex-shrink-0">
                        <Check size={16} />
                      </div>
                    )}
                  </div>
                  
                  <p className="text-xs text-gray-600 mb-2 line-clamp-2">{template.description}</p>
                  
                  <div className="flex items-center justify-between text-xs mb-2">
                    <div className="flex items-center gap-1">
                      <Star size={10} className="text-yellow-500" />
                      <span className="font-medium text-xs">ATS {template.ats_score}%</span>
                    </div>
                    <div className="flex items-center gap-1 text-gray-500">
                      <Zap size={10} />
                      <span className="text-xs">{template.category}</span>
                    </div>
                  </div>
                  
                  <div className="flex flex-wrap gap-1">
                    {template.industry.slice(0, 2).map((industry) => (
                      <span
                        key={industry}
                        className="px-1.5 py-0.5 bg-gray-100 text-gray-600 text-xs rounded"
                      >
                        {industry}
                      </span>
                    ))}
                    {template.industry.length > 2 && (
                      <span className="px-1.5 py-0.5 bg-gray-100 text-gray-600 text-xs rounded">
                        +{template.industry.length - 2}
                      </span>
                    )}
                  </div>
                </div>
                
                {/* Selection Overlay */}
                {currentTemplate === template.name && (
                  <div className="absolute inset-0 bg-emerald-500 bg-opacity-10 flex items-center justify-center">
                    <div className="bg-emerald-500 text-white rounded-full p-1.5">
                      <Check size={16} />
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
        
        <div className="p-6 border-t border-gray-200 bg-gray-50">
          <div className="flex justify-between items-center">
            <div className="text-sm text-gray-600">
              {displayTemplates.length} template{displayTemplates.length !== 1 ? 's' : ''} available
            </div>
            <div className="flex gap-3">
              <button
                onClick={onClose}
                className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
              >
                Cancel
              </button>
              <button
                onClick={onClose}
                className="px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700"
              >
                Apply Template
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
