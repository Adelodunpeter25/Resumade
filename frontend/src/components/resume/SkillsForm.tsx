import { memo } from 'react'
import { Plus, Trash2 } from 'lucide-react'
import type { Resume, Skill } from '../../types'

interface Props {
  data: Partial<Resume>
  onChange: (field: string, value: any) => void
}

function SkillsForm({ data, onChange }: Props) {
  const skills = data.skills || []

  const addSkill = () => {
    onChange('skills', [...skills, { name: '', level: '' }])
  }

  const updateSkill = (index: number, field: keyof Skill, value: any) => {
    const updated = [...skills]
    updated[index] = { ...updated[index], [field]: value }
    onChange('skills', updated)
  }

  const removeSkill = (index: number) => {
    onChange('skills', skills.filter((_, i) => i !== index))
  }

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-2 gap-4">
        {skills.map((skill, index) => (
          <div key={index} className="border border-gray-200 rounded-lg p-4 relative">
            <button
              onClick={() => removeSkill(index)}
              className="absolute top-2 right-2 p-1 text-red-600 hover:bg-red-50 rounded"
            >
              <Trash2 size={16} />
            </button>

            <div className="mb-3">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Skill Name *
              </label>
              <input
                type="text"
                value={skill.name}
                onChange={(e) => updateSkill(index, 'name', e.target.value)}
                placeholder="e.g., JavaScript, Project Management"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Proficiency Level
              </label>
              <select
                value={skill.level}
                onChange={(e) => updateSkill(index, 'level', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
              >
                <option value="">Do not specify</option>
                <option value="Beginner">Beginner</option>
                <option value="Intermediate">Intermediate</option>
                <option value="Advanced">Advanced</option>
                <option value="Expert">Expert</option>
              </select>
            </div>
          </div>
        ))}
      </div>

      <button
        onClick={addSkill}
        className="w-full flex items-center justify-center gap-2 px-4 py-3 border-2 border-dashed border-gray-300 rounded-lg hover:border-emerald-500 hover:bg-emerald-50 text-gray-600 hover:text-emerald-600"
      >
        <Plus size={20} />
        <span>Add Skill</span>
      </button>
    </div>
  )
}

export default memo(SkillsForm)
