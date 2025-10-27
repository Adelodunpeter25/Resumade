import { memo, useCallback, useState } from 'react'
import type { Resume } from '../../types'
import RichTextEditor from '../common/RichTextEditor'
import { Sparkles, Loader2 } from 'lucide-react'
import { useAISuggestions } from '../../hooks/useAISuggestions'

interface Props {
  data: Partial<Resume>
  onChange: (field: string, value: any) => void
}

function PersonalInfoForm({ data, onChange }: Props) {
  const [generatingSummary, setGeneratingSummary] = useState(false)
  const [summaryError, setSummaryError] = useState('')
  const { generateSummary } = useAISuggestions()

  const updateField = useCallback((field: string, value: string) => {
    onChange('personal_info', { ...data.personal_info, [field]: value })
  }, [data.personal_info, onChange])

  const handleGenerateSummary = async () => {
    const tagline = data.personal_info?.tagline
    if (!tagline) {
      setSummaryError('Please fill in your professional tagline first')
      return
    }

    setGeneratingSummary(true)
    setSummaryError('')

    try {
      // Extract position from tagline (first part before |)
      const position = tagline.split('|')[0].trim()
      
      // Get skills from resume if available
      const skills = (data.skills || []).map(s => s.name).slice(0, 8)
      
      // Estimate years of experience from experience section
      const yearsExp = data.experience?.length ? data.experience.length * 2 : 3

      const summary = await generateSummary(position, yearsExp, skills.length > 0 ? skills : ['various technical skills'])
      
      if (summary) {
        updateField('summary', summary)
      }
    } catch (err: any) {
      setSummaryError(err.message || 'Failed to generate summary')
    } finally {
      setGeneratingSummary(false)
    }
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

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Professional Tagline
        </label>
        <input
          type="text"
          value={data.personal_info?.tagline || ''}
          onChange={(e) => updateField('tagline', e.target.value)}
          placeholder="e.g., Senior Software Engineer | Full-Stack Developer"
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
        />
        <p className="mt-1 text-xs text-gray-500">A short headline that appears below your name</p>
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
        <div className="flex items-center justify-between mb-2">
          <label className="block text-sm font-medium text-gray-700">
            Professional Summary
          </label>
          <button
            type="button"
            onClick={handleGenerateSummary}
            disabled={generatingSummary || !data.personal_info?.tagline}
            className="flex items-center gap-1 text-sm text-purple-600 hover:text-purple-700 disabled:opacity-50 disabled:cursor-not-allowed"
            title={!data.personal_info?.tagline ? 'Fill in professional tagline first' : 'Generate AI summary'}
          >
            {generatingSummary ? (
              <>
                <Loader2 size={16} className="animate-spin" />
                Generating...
              </>
            ) : (
              <>
                <Sparkles size={16} />
                Generate with AI
              </>
            )}
          </button>
        </div>
        <RichTextEditor
          value={data.personal_info?.summary || ''}
          onChange={(value) => updateField('summary', value)}
          placeholder="Brief overview of your professional background and career goals..."
        />
        <p className="text-xs text-gray-500 mt-1">
          Tip: A strong summary highlights your experience and key skills. Click "Generate with AI" for help!
        </p>
        {summaryError && (
          <p className="text-xs text-red-600 mt-1">{summaryError}</p>
        )}
      </div>
    </div>
  )
}

export default memo(PersonalInfoForm)
