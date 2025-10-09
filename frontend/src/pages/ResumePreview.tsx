import { useState, useEffect } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { ArrowLeft, Download, RefreshCw } from 'lucide-react'
import { resumeService } from '../services'
import type { Resume, Template } from '../types'

export default function ResumePreview() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [resume, setResume] = useState<Resume | null>(null)
  const [templates, setTemplates] = useState<Template[]>([])
  const [selectedTemplate, setSelectedTemplate] = useState<string>('')
  const [previewUrl, setPreviewUrl] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)
  const [downloading, setDownloading] = useState(false)

  useEffect(() => {
    if (id) {
      loadData()
    }
  }, [id])

  useEffect(() => {
    if (selectedTemplate && id) {
      loadPreview()
    }
  }, [selectedTemplate, id])

  const loadData = async () => {
    try {
      const [resumeRes, templatesRes] = await Promise.all([
        resumeService.getResume(Number(id)),
        resumeService.getTemplates()
      ])

      if (resumeRes.success && resumeRes.data) {
        setResume(resumeRes.data)
        setSelectedTemplate(resumeRes.data.template_name)
      }

      if (templatesRes.success && templatesRes.data) {
        setTemplates(templatesRes.data)
      }
    } catch (err) {
      alert('Failed to load data')
      navigate('/dashboard')
    } finally {
      setLoading(false)
    }
  }

  const loadPreview = async () => {
    if (previewUrl) {
      window.URL.revokeObjectURL(previewUrl)
    }

    try {
      const blob = await resumeService.previewTemplate(selectedTemplate, Number(id))
      const url = window.URL.createObjectURL(blob)
      setPreviewUrl(url)
    } catch (err) {
      alert('Failed to load preview')
    }
  }

  const handleDownload = async () => {
    if (!resume) return

    setDownloading(true)
    try {
      const blob = await resumeService.downloadPDF(Number(id), selectedTemplate)
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `${resume.title}.pdf`
      a.click()
      window.URL.revokeObjectURL(url)
    } catch (err) {
      alert('Failed to download PDF')
    } finally {
      setDownloading(false)
    }
  }

  useEffect(() => {
    return () => {
      if (previewUrl) {
        window.URL.revokeObjectURL(previewUrl)
      }
    }
  }, [previewUrl])

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
                onClick={() => navigate(`/resume/${id}`)}
                className="p-2 hover:bg-gray-100 rounded-lg"
              >
                <ArrowLeft size={20} />
              </button>
              <div>
                <h1 className="text-xl font-bold text-gray-900">Preview & Download</h1>
                <p className="text-sm text-gray-500">{resume?.title}</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <button
                onClick={loadPreview}
                className="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
              >
                <RefreshCw size={20} />
                <span>Refresh</span>
              </button>
              <button
                onClick={handleDownload}
                disabled={downloading}
                className="flex items-center gap-2 bg-gradient-to-r from-emerald-600 to-teal-600 text-white px-4 py-2 rounded-lg hover:from-emerald-700 hover:to-teal-700 disabled:opacity-50"
              >
                <Download size={20} />
                <span>{downloading ? 'Downloading...' : 'Download PDF'}</span>
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-12 gap-6">
          {/* Template Selector */}
          <div className="col-span-3">
            <div className="bg-white rounded-lg shadow p-4 sticky top-8">
              <h3 className="font-semibold text-gray-900 mb-4">Select Template</h3>
              <div className="space-y-2">
                {templates.map((template) => (
                  <button
                    key={template.name}
                    onClick={() => setSelectedTemplate(template.name)}
                    className={`w-full text-left px-4 py-3 rounded-lg transition-colors ${
                      selectedTemplate === template.name
                        ? 'bg-emerald-50 text-emerald-600 font-medium border-2 border-emerald-600'
                        : 'bg-gray-50 text-gray-700 hover:bg-gray-100 border-2 border-transparent'
                    }`}
                  >
                    <div className="font-medium">{template.display_name}</div>
                    <div className="text-xs text-gray-500 mt-1">{template.description}</div>
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* PDF Preview */}
          <div className="col-span-9">
            <div className="bg-white rounded-lg shadow overflow-hidden">
              {previewUrl ? (
                <iframe
                  src={previewUrl}
                  className="w-full h-[calc(100vh-200px)] border-0"
                  title="Resume Preview"
                />
              ) : (
                <div className="flex items-center justify-center h-[calc(100vh-200px)]">
                  <div className="text-center">
                    <div className="w-16 h-16 border-4 border-emerald-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
                    <p className="text-gray-600">Loading preview...</p>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
