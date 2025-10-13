import { useState, useEffect } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { ArrowLeft, Check, Eye } from 'lucide-react'
import { resumeService } from '../services'
import type { Template } from '../types'

export default function TemplateSelector() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [templates, setTemplates] = useState<Template[]>([])
  const [selectedTemplate, setSelectedTemplate] = useState<string>('')
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [previewUrl, setPreviewUrl] = useState<string | null>(null)

  useEffect(() => {
    loadTemplates()
  }, [])

  const loadTemplates = async () => {
    try {
      const response = await resumeService.getTemplates()
      if (response.success && response.data) {
        setTemplates(response.data.all_templates || [])
      }
    } catch (err) {
      alert('Failed to load templates')
    } finally {
      setLoading(false)
    }
  }

  const handlePreview = async (templateName: string) => {
    try {
      const blob = await resumeService.previewTemplate(templateName, id ? Number(id) : undefined)
      const url = window.URL.createObjectURL(blob)
      setPreviewUrl(url)
    } catch (err) {
      alert('Failed to preview template')
    }
  }

  const handleApply = async () => {
    if (!selectedTemplate || !id) return

    setSaving(true)
    try {
      await resumeService.updateResume(Number(id), { template_name: selectedTemplate })
      navigate(`/resume/${id}`)
    } catch (err) {
      alert('Failed to apply template')
    } finally {
      setSaving(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="w-16 h-16 border-4 border-emerald-600 border-t-transparent rounded-full animate-spin"></div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center gap-4">
              <button
                onClick={() => navigate(id ? `/resume/${id}` : '/dashboard')}
                className="p-2 hover:bg-gray-100 rounded-lg"
              >
                <ArrowLeft size={20} />
              </button>
              <h1 className="text-xl font-bold text-gray-900">Choose Template</h1>
            </div>
            {selectedTemplate && id && (
              <button
                onClick={handleApply}
                disabled={saving}
                className="bg-gradient-to-r from-emerald-600 to-teal-600 text-white px-6 py-2 rounded-lg hover:from-emerald-700 hover:to-teal-700 disabled:opacity-50"
              >
                {saving ? 'Applying...' : 'Apply Template'}
              </button>
            )}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {templates.map((template) => (
            <div
              key={template.name}
              className={`bg-white rounded-lg shadow overflow-hidden cursor-pointer transition-all ${
                selectedTemplate === template.name
                  ? 'ring-4 ring-emerald-500'
                  : 'hover:shadow-lg'
              }`}
              onClick={() => setSelectedTemplate(template.name)}
            >
              {/* Template Preview Image */}
              <div className="aspect-[8.5/11] bg-gray-100 relative">
                <img
                  src={template.preview_url}
                  alt={template.display_name}
                  className="w-full h-full object-cover"
                  onError={(e) => {
                    e.currentTarget.src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 280"%3E%3Crect fill="%23f3f4f6" width="200" height="280"/%3E%3Ctext x="50%25" y="50%25" text-anchor="middle" fill="%239ca3af" font-size="16"%3EPreview%3C/text%3E%3C/svg%3E'
                  }}
                />
                {selectedTemplate === template.name && (
                  <div className="absolute top-4 right-4 bg-emerald-600 text-white p-2 rounded-full">
                    <Check size={20} />
                  </div>
                )}
              </div>

              {/* Template Info */}
              <div className="p-4">
                <h3 className="font-semibold text-gray-900 mb-1">
                  {template.display_name}
                </h3>
                <p className="text-sm text-gray-600 mb-3">
                  {template.description}
                </p>
                <button
                  onClick={(e) => {
                    e.stopPropagation()
                    handlePreview(template.name)
                  }}
                  className="w-full flex items-center justify-center gap-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
                >
                  <Eye size={16} />
                  <span>Preview</span>
                </button>
              </div>
            </div>
          ))}
        </div>
      </main>

      {/* Preview Modal */}
      {previewUrl && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
          onClick={() => {
            window.URL.revokeObjectURL(previewUrl)
            setPreviewUrl(null)
          }}
        >
          <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-auto">
            <div className="sticky top-0 bg-white border-b border-gray-200 p-4 flex justify-between items-center">
              <h3 className="text-lg font-semibold">Template Preview</h3>
              <button
                onClick={() => {
                  window.URL.revokeObjectURL(previewUrl)
                  setPreviewUrl(null)
                }}
                className="text-gray-500 hover:text-gray-700"
              >
                ✕
              </button>
            </div>
            <div className="p-4">
              <iframe
                src={previewUrl}
                className="w-full h-[80vh] border-0"
                title="Template Preview"
              />
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
