import { memo } from 'react'
import { useState } from 'react';
import type { Resume } from '../../types';
import RichTextEditor from '../common/RichTextEditor';
import { Plus, Trash2 } from 'lucide-react';

interface Props {
  data: Partial<Resume>;
  onChange: (field: string, value: any) => void;
}

function ExperienceForm({ data, onChange }: Props) {
  const [experiences, setExperiences] = useState(data.experience || []);

  const addExperience = () => {
    const newExperience = {
      company: '',
      position: '',
      location: '',
      start_date: '',
      end_date: '',
      description: '',
      current: false
    };
    const updatedExperiences = [...experiences, newExperience];
    setExperiences(updatedExperiences);
    onChange('experience', updatedExperiences);
  };

  const updateExperience = (index: number, field: string, value: any) => {
    const updatedExperiences = experiences.map((exp, i) => {
      if (i === index) {
        return { ...exp, [field]: value };
      }
      return exp;
    });
    setExperiences(updatedExperiences);
    onChange('experience', updatedExperiences);
  };

  const removeExperience = (index: number) => {
    const updatedExperiences = experiences.filter((_, i) => i !== index);
    setExperiences(updatedExperiences);
    onChange('experience', updatedExperiences);
  };

  return (
    <div className="space-y-8">
      {experiences.map((experience, index) => (
        <div key={index} className="p-6 bg-gray-50 rounded-lg space-y-6">
          <div className="flex justify-between items-center">
            <h3 className="text-lg font-medium text-gray-900">Experience {index + 1}</h3>
            <button
              onClick={() => removeExperience(index)}
              className="text-red-600 hover:text-red-700"
            >
              <Trash2 size={20} />
            </button>
          </div>

          <div className="grid grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Company *
              </label>
              <input
                type="text"
                value={experience.company}
                onChange={(e) => updateExperience(index, 'company', e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Position *
              </label>
              <input
                type="text"
                value={experience.position}
                onChange={(e) => updateExperience(index, 'position', e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
                required
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Start Date *
              </label>
              <input
                type="month"
                value={experience.start_date}
                onChange={(e) => updateExperience(index, 'start_date', e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                End Date
              </label>
              <div className="space-y-2">
                <input
                  type="month"
                  value={experience.end_date}
                  onChange={(e) => updateExperience(index, 'end_date', e.target.value)}
                  disabled={experience.current}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent disabled:bg-gray-100"
                />
                <div className="flex items-center">
                  <input
                    type="checkbox"
                    id={`current-${index}`}
                    checked={experience.current}
                    onChange={(e) => {
                      updateExperience(index, 'current', e.target.checked);
                      if (e.target.checked) {
                        updateExperience(index, 'end_date', '');
                      }
                    }}
                    className="h-4 w-4 text-emerald-600 focus:ring-emerald-500 border-gray-300 rounded"
                  />
                  <label htmlFor={`current-${index}`} className="ml-2 text-sm text-gray-700">
                    I currently work here
                  </label>
                </div>
              </div>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Location
            </label>
            <input
              type="text"
              value={experience.location}
              onChange={(e) => updateExperience(index, 'location', e.target.value)}
              placeholder="City, State or Remote"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Description *
            </label>
            <RichTextEditor
              value={experience.description}
              onChange={(content) => updateExperience(index, 'description', content)}
              placeholder="Describe your responsibilities and achievements..."
            />
          </div>
        </div>
      ))}

      <button
        type="button"
        onClick={addExperience}
        className="flex items-center justify-center w-full px-4 py-3 border-2 border-dashed border-gray-300 rounded-lg text-gray-600 hover:border-emerald-500 hover:text-emerald-500 transition-colors"
      >
        <Plus size={20} className="mr-2" />
        Add Experience
      </button>
    </div>
  );
}

export default memo(ExperienceForm)
