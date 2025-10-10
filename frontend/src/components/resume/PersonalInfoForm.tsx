import type { Resume } from '../../types'
import RichTextEditor from '../common/RichTextEditor'

interface Props {
  data: Partial<Resume>
  onChange: (field: string, value: any) => void
}

export default function PersonalInfoForm({ data, onChange }: Props) {
  const updateField = (field: string, value: string) => {
    onChange('personal_info', { ...data.personal_info, [field]: value })
  }

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-2 gap-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Full Name *
          </label>
          <input
            type="text"
            value={data.personal_info?.full_name || ''}
            onChange={(e) => updateField('full_name', e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Email *
          </label>
          <input
            type="email"
            value={data.personal_info?.email || ''}
            onChange={(e) => updateField('email', e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
            required
          />
        </div>
      </div>

      <div className="grid grid-cols-2 gap-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Phone *
          </label>
          <input
            type="tel"
            value={data.personal_info?.phone || ''}
            onChange={(e) => updateField('phone', e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Location *
          </label>
          <input
            type="text"
            value={data.personal_info?.location || ''}
            onChange={(e) => updateField('location', e.target.value)}
            placeholder="City, State"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
            required
          />
        </div>
      </div>

      <div className="grid grid-cols-2 gap-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            LinkedIn
          </label>
          <input
            type="url"
            value={data.personal_info?.linkedin || ''}
            onChange={(e) => updateField('linkedin', e.target.value)}
            placeholder="https://linkedin.com/in/username"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Website
          </label>
          <input
            type="url"
            value={data.personal_info?.website || ''}
            onChange={(e) => updateField('website', e.target.value)}
            placeholder="https://yourwebsite.com"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
          />
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Professional Summary
        </label>
        <RichTextEditor
          value={data.personal_info?.summary || ''}
          onChange={(value) => updateField('summary', value)}
          placeholder="Brief overview of your professional background and career goals..."
        />
      </div>
    </div>
  )
}
